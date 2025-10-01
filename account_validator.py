"""
Account Validator Module
Detects and validates CP codes across position and trade files
"""

import io
import logging
from typing import Optional, Tuple, Dict
import pandas as pd
from account_config import ACCOUNT_REGISTRY, get_account_by_cp_code, get_all_cp_codes

logger = logging.getLogger(__name__)


class AccountValidator:
    """Validates account consistency across files"""

    def __init__(self):
        self.position_account = None
        self.trade_account = None
        self.validation_errors = []

    def detect_account_in_file(self, file_content, file_type: str = "unknown") -> Optional[Dict]:
        """
        Detect CP code in file content

        Args:
            file_content: File content (bytes or text)
            file_type: "position" or "trade" for logging

        Returns:
            Account dict if found, None otherwise
        """
        try:
            # Convert file content to searchable text
            if isinstance(file_content, bytes):
                # Try to decode as text
                try:
                    search_text = file_content.decode('utf-8', errors='ignore')
                except:
                    search_text = str(file_content)
            else:
                search_text = str(file_content)

            # Normalize text for searching: uppercase, remove extra whitespace
            search_text_normalized = ' '.join(search_text.upper().split())

            # Search for each known CP code (case-insensitive, whitespace-tolerant)
            found_codes = []
            for cp_code in get_all_cp_codes():
                # Normalize CP code for comparison
                cp_code_normalized = cp_code.upper().replace(' ', '')

                # Also check with spaces removed from search text
                search_text_no_spaces = search_text_normalized.replace(' ', '')

                # Try multiple variations
                if (cp_code.upper() in search_text_normalized or
                    cp_code_normalized in search_text_no_spaces or
                    cp_code in search_text):  # Original case-sensitive as fallback
                    found_codes.append(cp_code)

            # Validation
            if len(found_codes) == 0:
                logger.warning(f"No CP code found in {file_type} file")
                return None

            if len(found_codes) > 1:
                logger.error(f"Multiple CP codes found in {file_type} file: {found_codes}")
                self.validation_errors.append(
                    f"Multiple accounts detected in {file_type} file: {', '.join(found_codes)}"
                )
                return None

            # Single CP code found
            cp_code = found_codes[0]
            account = get_account_by_cp_code(cp_code)
            logger.info(f"Detected account in {file_type} file: {account['name']} ({cp_code})")
            return account

        except Exception as e:
            logger.error(f"Error detecting account in {file_type} file: {e}")
            return None

    def detect_account_in_position_file(self, file_obj) -> Optional[Dict]:
        """
        Detect account in position file

        Args:
            file_obj: Uploaded file object from streamlit

        Returns:
            Account dict if found, None otherwise
        """
        try:
            # Read file content
            file_obj.seek(0)
            content = file_obj.read()
            file_obj.seek(0)  # Reset for later use

            account = self.detect_account_in_file(content, "position")
            self.position_account = account
            return account

        except Exception as e:
            logger.error(f"Error reading position file for account detection: {e}")
            return None

    def detect_account_in_trade_file(self, file_obj) -> Optional[Dict]:
        """
        Detect account in trade file

        Args:
            file_obj: Uploaded file object from streamlit

        Returns:
            Account dict if found, None otherwise
        """
        try:
            # Read file content
            file_obj.seek(0)
            content = file_obj.read()
            file_obj.seek(0)  # Reset for later use

            account = self.detect_account_in_file(content, "trade")
            self.trade_account = account
            return account

        except Exception as e:
            logger.error(f"Error reading trade file for account detection: {e}")
            return None

    def validate_account_match(self) -> Tuple[bool, str, str]:
        """
        Validate that position and trade files are from same account

        Returns:
            (is_valid, status_type, message)
            status_type: "success", "warning", "error"
        """
        pos_acc = self.position_account
        trade_acc = self.trade_account

        # Case 1: Both files have same account (GOOD!)
        if pos_acc and trade_acc and pos_acc['cp_code'] == trade_acc['cp_code']:
            return True, "success", f"✅ Account validated: {pos_acc['name']} ({pos_acc['cp_code']})"

        # Case 2: Mismatch between known accounts (BLOCK!)
        if pos_acc and trade_acc and pos_acc['cp_code'] != trade_acc['cp_code']:
            msg = (
                f"❌ ACCOUNT MISMATCH DETECTED!\n\n"
                f"Position File: {pos_acc['name']} ({pos_acc['cp_code']})\n"
                f"Trade File: {trade_acc['name']} ({trade_acc['cp_code']})\n\n"
                f"Cannot process files from different accounts.\n"
                f"Please upload matching files."
            )
            return False, "error", msg

        # Case 3: Multiple accounts in one file (BLOCK!)
        if self.validation_errors:
            return False, "error", "\n".join(self.validation_errors)

        # Case 4: One file has account, other doesn't (WARN)
        if pos_acc and not trade_acc:
            msg = (
                f"⚠️ Account detected in position file only: {pos_acc['name']} ({pos_acc['cp_code']})\n"
                f"Trade file CP code not found. Proceeding with caution."
            )
            return True, "warning", msg

        if trade_acc and not pos_acc:
            msg = (
                f"⚠️ Account detected in trade file only: {trade_acc['name']} ({trade_acc['cp_code']})\n"
                f"Position file CP code not found. Proceeding with caution."
            )
            return True, "warning", msg

        # Case 5: Neither file has detectable account (WARN)
        if not pos_acc and not trade_acc:
            msg = (
                f"⚠️ No CP code detected in either file.\n"
                f"Cannot verify account consistency. Proceeding with caution."
            )
            return True, "warning", msg

        # Default fallback
        return True, "warning", "Account validation inconclusive"

    def get_account_info(self) -> Optional[Dict]:
        """Get the detected account info (position file takes precedence)"""
        return self.position_account or self.trade_account

    def get_account_prefix(self) -> str:
        """Get account name for file prefixing, returns empty string if unknown"""
        account = self.get_account_info()
        return f"{account['name']}_" if account else ""

    def reset(self):
        """Reset validator state"""
        self.position_account = None
        self.trade_account = None
        self.validation_errors = []
