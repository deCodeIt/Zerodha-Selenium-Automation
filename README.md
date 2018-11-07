# Kite-Zerodha Selenium automation

> Have you computer manage your protfolio when you work/sleep

> Kite Zerodha order automation with Entry/Target/StopLoss price by giving in a simple portfolio

---

## Additional Files

> Don't forget to create a `credentials.json` file as below

```json
{
   "username":"ABC123",
   "password":"thisIsMyPassword",
   "security": {
      "Who is your spouse's email service provider? (e.g. gmail, rediffmail, etc)" : "yourAnswer",
      "What is your mother's name?":"yourAnswer",
      "What was the brand of your first mobile?":"yourAnswer",
      "What is the name of your first child?":"yourAnswer",
      "In Which bank did you first open your account? ( e.g. HDFC ,SBI, etc.)":"yourAnswer"
   }
}
```

---

## Requriements

- See `requirements.txt` for dependencies

## Features

The idea is to have a Excel/CSV file whereIn your stockName,EntryPrice,Target,SL,Quantity would be mentioned.
This script will be like a daemon/cron-job to regularly check for updates and place buy/sell order automatically without user intervention thereby giving freedom to user to continue working on his/her stuff ( or sleep zzzZZZZ )

## Usage

- Run the script using `python zerodha.py`

---

## Support

Reach out to me at one of the following places!

- Facebook at <a href="https://www.facebook.com/theAliJafri" target="_blank">`@theAliJafri`</a>

---

## Donations (Optional)

- PhonePe: decodeit@ybl


---

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2018 © <a href="#">Ali Jafri</a>.
