# Start the PostgreSQL service
sudo service postgresql start

# Activate the virtual environment
source venv/bin/activate

# Run the Streamlit app
streamlit run app/main.py
