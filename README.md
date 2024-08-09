# Business Dashboard 📊

Transform your business data into insightful analytics effortlessly!

This Python-based dashboard is designed to provide comprehensive insights into your business operations. Whether you're analyzing customer behavior, sales trends, market performance, or product profitability, this tool simplifies the process and presents the data in an intuitive and interactive way.

## Prerequisites

Before using the Business Dashboard, ensure you have the following installed:

- **Python (version 3.x)**
- **Streamlit**: For creating the web application.
- **Pandas**: For data manipulation and analysis.
- **Altair**: For creating interactive visualizations.
- **Matplotlib**: For additional charting options.

## Functionalities

- **Customer Analytics**: Identify profitable customers, analyze payment methods, and interactively filter data.
- **Market Analytics**: Compare total and mean sales by market with interactive filtering.
- **Sales Analytics**: Analyze sales by product, visualize performance trends, and apply interactive filters.
- **Profitability Analytics**: Gain insights into profitability, visualize segment performance, and use interactive filters.
- **Product Analytics**: Identify top/least selling products, analyze category profits, and observe sales trends over time.

## Setup

1. **Clone the repository:**

    ```bash
    https://github.com/GriRonny/Python_Elective_FHNW.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd Python_Elective_FHNW
    ```

3. **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```

   If you encounter any issues while installing the requirements, you can try installing them directly in PyCharm:

    - Open PyCharm and navigate to `File > Settings > Project: YourProjectName > Python Interpreter`.
    - Click on the `+` button to open the package manager.
    - Search for the package you need to install (e.g., `streamlit`) and click on `Install Package`.

## How to use

1. **Navigate to the project directory:**

    ```bash
    cd Python_Elective_FHNW
    ```

2. **Run the application: enter in terminal**

    ```bash
    streamlit run main_dashboard.py
    ```

3. **Upload your data:**

    - Select the latest `global_superstore.csv` file.
    - Drag and drop the file into the upload area or click 'Browse files' to select it.

4. **Analyze your data:**

    - Choose the desired analysis section (e.g., Customer Analytics, Market Analytics).
    - Apply filters as needed to customize your insights.

5. **Switch between analysis views:**

    - Navigate through different views using the buttons provided in the interface.
    - Return to the upload page to analyze a different dataset as needed.
