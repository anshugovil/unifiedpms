# Email Notification Setup Guide

This guide will help you set up email notifications using SendGrid for your trade processing system.

## Prerequisites

- SendGrid account (free tier available)
- Verified sender email address

## Step 1: Install Dependencies

```bash
pip install sendgrid python-dotenv
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

## Step 2: Get SendGrid API Key

1. Go to [SendGrid](https://sendgrid.com) and create a free account
2. Navigate to **Settings** → **API Keys**
3. Click **Create API Key**
4. Give it a name (e.g., "Trade Processing")
5. Select **Full Access** permissions
6. Click **Create & View**
7. **Copy the API key** (you won't be able to see it again!)

## Step 3: Verify Sender Email

1. In SendGrid, go to **Settings** → **Sender Authentication**
2. Choose **Single Sender Verification** (easier) or **Domain Authentication** (better for production)
3. For Single Sender:
   - Click **Verify a Single Sender**
   - Fill in your details
   - Use an email you have access to (e.g., `noreply@yourdomain.com`)
   - Check your email and click the verification link

## Step 4: Configure Environment Variables

### Option A: Using .env file (Recommended)

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file:
   ```bash
   SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   SENDGRID_FROM_EMAIL=noreply@yourdomain.com
   SENDGRID_FROM_NAME=Trade Processing System
   ```

3. The app will automatically load these variables

### Option B: Using System Environment Variables

#### Windows (PowerShell):
```powershell
$env:SENDGRID_API_KEY="SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
$env:SENDGRID_FROM_EMAIL="noreply@yourdomain.com"
$env:SENDGRID_FROM_NAME="Trade Processing System"
```

#### Windows (Command Prompt):
```cmd
set SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
set SENDGRID_FROM_EMAIL=noreply@yourdomain.com
set SENDGRID_FROM_NAME=Trade Processing System
```

#### Linux/Mac:
```bash
export SENDGRID_API_KEY="SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export SENDGRID_FROM_EMAIL="noreply@yourdomain.com"
export SENDGRID_FROM_NAME="Trade Processing System"
```

## Step 5: Test Email Configuration

Run the test script:

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

## Step 6: Use in Streamlit App

1. Start the Streamlit app:
   ```bash
   streamlit run unified-streamlit-app.py
   ```

2. In the sidebar, you'll see **📧 Email Notifications** section

3. If configured correctly, you'll see: ✓ Email configured

4. Check the **"Send email on completion"** checkbox

5. Enter recipient email addresses (comma-separated)

6. Run your pipeline - emails will be sent automatically!

## Email Templates

The system includes pre-configured templates for:

- ✅ **Stage 1 Complete** - Trade processing completion with attachments
- 📊 **ACM Export Complete** - ACM file generation
- 💰 **Deliverables Report** - Physical deliverables calculation
- 📅 **Expiry Delivery** - Expiry settlement notifications
- 🔄 **Broker Reconciliation** - Broker recon results
- ❌ **Error Notifications** - Processing errors

## Email Attachments

Emails automatically include relevant files:
- CSV outputs (parsed trades, positions, etc.)
- Summary reports
- Missing mappings reports

**Note**: SendGrid has attachment size limits (30MB total). Large Excel files are not attached by default.

## Troubleshooting

### Email not sending

1. **Check API Key**: Make sure it's correct and has Full Access permissions
2. **Check Sender Email**: Must be verified in SendGrid
3. **Check Logs**: Look for error messages in console/terminal
4. **Free Tier Limits**: SendGrid free tier has 100 emails/day limit

### "Email not configured" message

1. Make sure environment variables are set
2. Restart the Streamlit app after setting variables
3. Check `.env` file syntax (no spaces around `=`)

### Emails going to spam

1. Use Domain Authentication instead of Single Sender (in SendGrid)
2. Add SPF/DKIM records to your domain
3. Warm up your sending reputation gradually

## SendGrid Free Tier Limits

- 100 emails per day
- Maximum 30MB total attachment size per email
- No time limit on the free tier

For production use with higher volumes, consider upgrading to a paid plan.

## Security Best Practices

1. ✅ **Never commit `.env` file** to git (already in .gitignore)
2. ✅ **Use environment-specific API keys** (dev vs production)
3. ✅ **Rotate API keys** periodically
4. ✅ **Use least-privilege permissions** (create separate API keys for different apps)
5. ✅ **Store production keys** in secure vault (Azure Key Vault, AWS Secrets Manager, etc.)

## Support

- SendGrid Documentation: https://docs.sendgrid.com
- SendGrid Support: https://support.sendgrid.com
- Project Issues: https://github.com/anthropics/claude-code/issues
