<!DOCTYPE html>
<html lang="en">
</head>
<body>
    <div class="container">
        <h1>🎉 Welcome to the MLTrader Project! 🎉</h1>
        <p>This project is a super cool machine learning-based trading strategy using the <code>lumibot</code> library and Alpaca's trading API. The strategy uses sentiment analysis to make smart trading decisions for the SPY symbol. 🚀</p>
        
 <h2>Project Structure 📂</h2>
        <pre>
.
├── stonks.py           # Main script containing the MLTrader strategy
├── README.html       # Project README in HTML format
└── utils.py          # Utility functions including sentiment estimation
        </pre>
        
<h2>Dependencies 📦</h2>
        <p>Make sure to install these dependencies before running the project:</p>
        <pre>
pip install lumibot alpaca-trade-api pandas numpy torch transformers
        </pre>
<h2>Setup 🛠️</h2>
        <p>To get started with the MLTrader project, follow these steps to set up your environment and get your API credentials from Alpaca:</p>
        
<h3>1. Obtain Alpaca API Credentials 🔑</h3>
        <ol>
            <li>Sign up for an account at <a href="https://alpaca.markets/">Alpaca</a>.</li>
            <li>Log in and navigate to the API section of your dashboard.</li>
            <li>Create a new API key. Choose paper trading to test without real money.</li>
            <li>Store your <code>API_KEY</code> and <code>API_SECRET</code> securely.</li>
        </ol>
        
<h3>2. Configure Your Environment 💻</h3>
        <p>It's best to use environment variables or a configuration file to store your API credentials securely. You can set your environment variables as follows:</p>
        <pre>
export ALPACA_API_KEY="your_api_key_here"
export ALPACA_API_SECRET="your_api_secret_here"
        </pre>
        <p>Alternatively, you can create a <code>config.py</code> file to store these values (not recommended for production).</p>
        
<h2>Usage 🚀</h2>
        <p>To run the backtesting process, execute the main script:</p>
        <pre>
python stonks.py
        </pre>
        <p>The backtesting will use historical data to simulate trading based on the MLTrader strategy. Ensure that your <code>utils.py</code> file includes the necessary functions for sentiment analysis, which are essential for the strategy's decision-making process.</p>
    
</body>
</html>
