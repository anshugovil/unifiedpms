# Email Configuration Setup

The application uses **Streamlit Secrets** to manage email credentials securely.

## Prerequisites

- SendGrid account (free tier available)
- Verified sender email address

## Step 1: Install Dependencies

```bash
pip install sendgrid
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

## Step 4: Configure Streamlit Secrets

### For Local Development:

1. Create `.streamlit` directory (if it doesn't exist):
   ```bash
   mkdir .streamlit
   ```

2. Create `.streamlit/secrets.toml` file:
   ```bash
   # Copy the example
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

3. Edit `.streamlit/secrets.toml` with your credentials:
   ```toml
   SENDGRID_API_KEY = "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"
   SENDGRID_FROM_EMAIL = "agovil@aurigincm.com"
   SENDGRID_FROM_NAME = "Aurigin Trade Processing"
   ```

### For Streamlit Cloud:

1. Deploy your app to Streamlit Cloud
2. Go to your app settings (⋮ menu → Settings)
3. Navigate to "Secrets" in the left sidebar
4. Add your secrets in TOML format:
   ```toml
   SENDGRID_API_KEY = "SG.your_api_key_here"
   SENDGRID_FROM_EMAIL = "agovil@aurigincm.com"
   SENDGRID_FROM_NAME = "Aurigin Trade Processing"
   ```
5. Save and restart the app

## Step 5: Use in Streamlit App

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

## Email Recipients

- **Default recipient**: `operations@aurigincm.com` (always included)
- **Additional recipients**: Can be added via UI (comma-separated)

## Troubleshooting

### "⚠️ Email not configured" warning

1. Check `.streamlit/secrets.toml` file exists
2. Verify all three keys are present (SENDGRID_API_KEY, SENDGRID_FROM_EMAIL, SENDGRID_FROM_NAME)
3. Check TOML syntax - values must be in quotes
4. Restart Streamlit app after creating/editing secrets

### Email not sending

1. **Check API Key**: Make sure it's correct and has Full Access permissions
2. **Check Sender Email**: `agovil@aurigincm.com` must be verified in SendGrid
3. **Check Logs**: Look for error messages in Streamlit console
4. **Free Tier Limits**: SendGrid free tier has 100 emails/day limit
5. **Check SendGrid Activity**: https://app.sendgrid.com/email_activity

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

1. ✅ **Never commit `.streamlit/secrets.toml`** to git (already in .gitignore)
2. ✅ **Use environment-specific API keys** (dev vs production)
3. ✅ **Rotate API keys** periodically
4. ✅ **Use Streamlit Cloud secrets** for production deployments
5. ✅ **Keep API keys confidential** - never share in public channels

## Support

- SendGrid Documentation: https://docs.sendgrid.com
- SendGrid Support: https://support.sendgrid.com
- Project Issues: https://github.com/anthropics/claude-code/issues
