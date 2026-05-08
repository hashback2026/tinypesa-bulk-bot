# TinyPesa Bulk STK Push Bot

A Flask web application for sending bulk M-Pesa STK Push notifications via the TinyPesa API.

## Features

- Web interface for entering multiple phone numbers
- Auto-formatting of phone numbers (07XX, +254, 254 formats)
- Real-time results dashboard
- Webhook support for payment confirmations
- Ready for GitHub + Render deployment

## Quick Start

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your TinyPesa credentials
4. Run: `python app.py`

## Deployment

### Render
1. Push to GitHub
2. Connect repository on Render
3. Add environment variables from `.env.example`
4. Deploy!

## TinyPesa Setup

1. Sign up at [tinypesa.com](https://tinypesa.com)
2. Get your API credentials from the dashboard
3. Set webhook URL to your deployed app + `/api/webhook`

## Usage

1. Enter amount per recipient
2. Paste phone numbers (one per line)
3. Click "Send STK Push to All"
4. Recipients receive M-Pesa PIN prompt on their phones
