Ledger Lens 🔭
A modern, interactive, and insightful dashboard for your plain-text accounting files. Turn your command-line ledger into a powerful visual analysis tool.

Ledger Lens parses your Ledger, hledger, or Beancount files and presents them in a beautiful and intuitive web interface, allowing you to slice, dice, and understand your financial data like never before.

(Replace this with a real screenshot of your application)

Table of Contents
About The Project

Key Features

Built With

Getting Started

Prerequisites

Installation

Usage

Configuration

Roadmap

Contributing

License

Contact

Acknowledgements

About The Project
Plain-text accounting is an incredibly powerful system for managing personal and small business finances. It's transparent, version-controllable, and future-proof. However, the command-line interface, while efficient, can make it difficult to get a high-level, visual overview of your financial health.

Ledger Lens solves this problem by providing a rich, browser-based frontend for your data. It does the hard work of parsing your journal files and crunching the numbers so you can focus on what matters: gaining insights from your financial history.

Key Features
✨ Interactive Dashboard: A clean, at-a-glance overview of your finances.
📊 Multiple Chart Types: Visualize expenses, income, and net worth with bar charts, line graphs, and pie charts.
🔍 Powerful Filtering: Filter your transactions by date range, account, payee, or tags.
📈 Net Worth Tracking: Watch your net worth grow over time.
💰 Income vs. Expense Analysis: Easily compare where your money is coming from and where it's going.
📂 Multi-File Support: Include multiple ledger files to build a complete financial picture.
🌐 Web-Based & Self-Hosted: Access your dashboard from any device on your local network.

Built With
This project is built with a modern tech stack for a fast and reliable experience.

Backend: Python with Flask / FastAPI

Frontend: React / Vue.js with Chart.js / D3.js

Ledger Parsing: hledger-lib / beancount

Database (Optional): SQLite for caching/user data

Getting Started
Follow these instructions to get a local copy up and running.

Prerequisites
You will need the following software installed on your machine:

Python 3.8+ and Pip

Node.js v16+ and npm

Git

Installation
Clone the repository:

Bash

git clone https://github.com/your_username/ledger-lens.git
cd ledger-lens
Install backend dependencies:

Bash

pip install -r requirements.txt
Install frontend dependencies and build:

Bash

cd frontend
npm install
npm run build
cd ..
Run the application:

Bash

python main.py --file /path/to/your/journal.dat
Usage
Once the server is running, open your web browser and navigate to http://127.0.0.1:5000.

Command-Line Arguments
--file <path>: (Required) Path to your main ledger file.

--port <port>: Port to run the web server on. Defaults to 5000.

--host <host>: Host to bind the server to. Defaults to 127.0.0.1.

--debug: Run the server in debug mode.

Example:

Bash

python main.py --file "~/Documents/Finances/2025.ledger" --port 8080
Configuration
You can configure Ledger Lens using a config.yml file in the root directory. This allows you to set default file paths, currency symbols, date formats, and more without using command-line flags every time.

Example config.yml:

YAML

# Default path to your ledger file

ledger_file: "/home/user/finances/main.ledger"

# Default currency to display

display_currency: "USD"

# Date format (strftime)

date_format: "%Y-%m-%d"
Roadmap
See the open issues for a list of proposed features and known issues.

[ ] Beancount file support

[ ] Budgeting: Track spending against monthly or yearly budgets

[ ] Investment tracking and performance visualization

[ ] Docker support for easy deployment

[ ] Multi-user support with authentication

Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

Please see CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

License
Distributed under the MIT License. See LICENSE for more information.

Contact
Your Name - @YourTwitterHandle - your.email@example.com

Project Link: https://github.com/your_username/ledger-lens

Acknowledgements
The creators and maintainers of Ledger, hledger, and Beancount.

Shields.io for the cool badges.

Choose an Open Source License for the license guide.
