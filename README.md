
#Złota Koza Bot

Złota Koza Bot is the ultimate Telegram bot designed exclusively for dairy farmers to track their daily income efficiently. It empowers farmers to easily record and store their income data in a database for hassle-free retrieval and analysis.

#Features
Złota Koza Bot boasts the following features:

Add daily income by specifying the income and category
View daily and monthly income statistics
View a list of recent income records
Delete income records

Usage
To start the bot, simply run the main.py script:
python```
python main.py```

#Once the bot is running, you can interact with it using the following commands:

/start: Receive a warm welcome message and a list of available commands.

/help: Get a comprehensive list of available commands.

/dochod <amount> <category>: Add a daily income record.

/today: Get your daily income statistics.

/month: Get your monthly income statistics.

/dochody: Retrieve a list of recent income records.

/del<id>: Delete an income record (replace <id> with the record ID).

Categories
The categories.py file comprises a list of available income categories. You can modify this file to add or remove categories as needed. Each category has a unique codename and a list of aliases that can be used to refer to the category when adding income records.

We hope that you find Złota Koza Bot useful and efficient in managing your daily income data. Feel free to customize the bot to suit your specific requirements and add any additional features that you deem relevant for your farming business.
