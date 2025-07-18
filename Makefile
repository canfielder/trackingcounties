.PHONY: run install clean

# Run the Streamlit app
run:
	streamlit run app/app.py

# Install the tracking_counties package in editable mode
install:
	pip install -e tracking_counties

# Remove build artifacts
clean:
	rm -rf tracking_counties/build tracking_counties/dist tracking_counties.egg-info
