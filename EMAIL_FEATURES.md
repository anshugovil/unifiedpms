# Email Notification Features

## Overview

The trade processing system now supports automated email notifications via SendGrid. Emails are sent automatically when processing completes, with relevant reports attached.

## ✨ Features

### 📧 Automatic Email Sending

- **Stage 1 Completion**: Email with all output files when trade processing completes
- **Optional**: Enable/disable via Streamlit UI checkbox
- **Flexible Recipients**: Enter multiple email addresses (comma-separated)
- **Professional Templates**: Pre-designed HTML email templates

### 📎 Automatic Attachments

Emails automatically include:
- Parsed trades CSV
- Starting positions CSV
- Processed trades CSV
- Final positions CSV
- Summary report (TXT)
- Missing mappings report (if any)
- Mapping template (if needed)

### 🎨 Email Templates Available

1. **stage1_complete** - Trade processing completion
2. **acm_complete** - ACM export completion
3. **deliverables_complete** - Deliverables calculation
4. **expiry_delivery** - Expiry settlement alerts
5. **broker_recon** - Broker reconciliation results
6. **error_notification** - Processing error alerts
7. **custom** - Custom emails

## 📁 New Files Created

### Core Email Files

1. **`email_config.py`** - Email configuration and templates
   - EmailConfig class for settings
   - Pre-defined email templates
   - Environment variable loading

2. **`email_sender.py`** - SendGrid email sender
   - EmailSender class with SendGrid API
   - Template-based sending
   - Attachment handling
   - MIME type detection

3. **`EMAIL_SETUP.md`** - Setup instructions
   - Step-by-step SendGrid setup
   - Environment variable configuration
   - Testing and troubleshooting

4. **`.env.example`** - Environment variable template
   - Example configuration values
   - Copy to `.env` to use

5. **`EMAIL_FEATURES.md`** - This file
   - Feature documentation
   - Usage examples

### Updated Files

1. **`output_generator.py`**
   - Added email parameters to `save_all_outputs()`
   - Added `_send_completion_email()` method
   - Optional email integration

2. **`unified-streamlit-app.py`**
   - Email configuration UI in sidebar
   - Email toggle checkbox
   - Recipient input field
   - Setup instructions expander

3. **`requirements.txt`**
   - Added `sendgrid>=6.10.0`
   - Added `python-dotenv>=1.0.0`

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install sendgrid python-dotenv
```

### 2. Configure SendGrid

```bash
# Copy example file
cp .env.example .env

# Edit .env with your credentials
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SENDGRID_FROM_EMAIL=noreply@yourdomain.com
SENDGRID_FROM_NAME=Trade Processing System
```

### 3. Use in Streamlit

1. Start app: `streamlit run unified-streamlit-app.py`
2. Check "Send email on completion" in sidebar
3. Enter recipient emails
4. Run pipeline!

## 💻 Programmatic Usage

### Basic Email Sending

```python
from email_sender import EmailSender

sender = EmailSender()

# Send simple email
sender.send_email(
    to_emails=['user@example.com'],
    subject='Test Email',
    html_body='<h1>Hello!</h1><p>This is a test.</p>'
)
```

### Using Templates

```python
# Send Stage 1 completion email
sender.send_stage1_complete(
    to_emails=['user@example.com'],
    account_prefix='AURIGIN_',
    timestamp='20250103_143022',
    output_files={
        'parsed_trades': Path('output_1_parsed_trades.csv'),
        'processed_trades': Path('output_3_processed_trades.csv')
    },
    stats={
        'total_trades': 150,
        'starting_positions': 45,
        'final_positions': 52
    }
)
```

### Custom Email with Attachments

```python
sender.send_email(
    to_emails=['user@example.com'],
    subject='Custom Report',
    html_body='<p>Please find the reports attached.</p>',
    attachments=[
        Path('report1.csv'),
        Path('report2.xlsx')
    ],
    cc_emails=['manager@example.com']
)
```

### Error Notifications

```python
try:
    # Your processing code
    process_trades()
except Exception as e:
    sender.send_error_notification(
        to_emails=['admin@example.com'],
        error_type='Processing Error',
        error_message=str(e),
        error_trace=traceback.format_exc()
    )
```

## 🔧 Configuration Options

### Environment Variables

```bash
# Required
SENDGRID_API_KEY=your_api_key          # SendGrid API key
SENDGRID_FROM_EMAIL=your@email.com     # Verified sender email

# Optional
SENDGRID_FROM_NAME=Your Name           # Sender display name
EMAIL_RECIPIENTS=user1@ex.com,user2@ex.com  # Default recipients
```

### In Code

```python
from email_config import EmailConfig

# Custom configuration
config = EmailConfig(
    sendgrid_api_key='SG.xxx',
    from_email='custom@email.com',
    from_name='Custom Name'
)

sender = EmailSender(config)
```

## 📊 Email Content

### Stage 1 Completion Email

**Subject**: ✅ Trade Processing Complete - AURIGIN_20250103_143022

**Body includes**:
- Account prefix
- Processing timestamp
- Total trades processed
- Starting/final position counts
- List of attached files
- Professional HTML formatting

**Attachments**:
- All CSV output files
- Summary report
- Missing mappings (if any)

### Deliverables Email

**Subject**: 📊 Deliverables Report - AURIGIN_20250103_143022

**Body includes**:
- Total underlyings analyzed
- Net deliverables summary
- Deliverables file attached

### Error Email

**Subject**: ❌ Processing Error - [Error Type]

**Body includes**:
- Error type and message
- Timestamp
- Full error trace
- Red highlighting for urgency

## 🔒 Security

- ✅ `.env` file is in `.gitignore` (never committed)
- ✅ API keys never logged
- ✅ Environment-based configuration
- ✅ Optional email feature (graceful degradation)

## 📈 SendGrid Limits

### Free Tier
- 100 emails/day
- 30MB max attachment size per email
- Unlimited time period

### Recommendations
- For production: Consider paid plan
- Monitor daily quota usage
- Set up usage alerts in SendGrid dashboard

## 🧪 Testing

### Test Configuration

```bash
python email_sender.py
```

Expected output:
```
Email Configuration Test
==================================================
Configured: True
API Key: ***xxxx
From Email: noreply@yourdomain.com
From Name: Trade Processing System
==================================================

Email sending enabled: True
```

### Test Email Send

```python
from email_sender import EmailSender

sender = EmailSender()

if sender.is_enabled():
    sender.send_email(
        to_emails=['your@email.com'],
        subject='Test',
        html_body='<h1>Test successful!</h1>'
    )
```

## 🐛 Troubleshooting

### "Email not configured"
- Check environment variables are set
- Verify `.env` file location
- Restart Streamlit app

### "Email send failed"
- Verify API key is correct
- Check sender email is verified in SendGrid
- Review SendGrid activity log

### Emails in spam
- Use Domain Authentication (not Single Sender)
- Add SPF/DKIM records
- Warm up sending reputation

## 📞 Support

- SendGrid Docs: https://docs.sendgrid.com
- API Reference: https://docs.sendgrid.com/api-reference
- Support: https://support.sendgrid.com

## 🎯 Future Enhancements

Potential future features:
- [ ] Scheduled email reports
- [ ] Email digest (summary of multiple runs)
- [ ] Customizable templates via UI
- [ ] Email delivery tracking
- [ ] Multiple recipient groups
- [ ] Email preview before sending
