---
title: "Install PostgreSQL 14.7 for macOS"
description: "Install PostgreSQL 14.7 for macOS"
summary: ""
date: 2023-09-07T16:13:18+02:00
lastmod: 2023-09-07T16:13:18+02:00
draft: false
weight: 910
toc: true
seo:
  title: "Install PostgreSQL 14.7 for macOS" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  robots: "" # custom robot tags (optional)
---

In this guide, you will learn how to set up PostgreSQL 14.7 on your MacBook using Homebrew, a widely-used package manager for macOS. The steps are straightforward and include:

1. Install Homebrew
2. Install PostgreSQL
3. Download the Northwind PostgreSQL SQL file
4. Create a New PostgreSQL Database
5. Import the Northwind SQL file
6. Verify the Northwind database installation
7. Connect to the Database Using Jupyter Notebook

## Prerequisites

Ensure you have a MacBook or iMac running macOS 10.13 or later.

**Install Xcode Command Line Tools**
To start, you need to install the Xcode Command Line Tools, which are essential for software development on your Mac.

1. Open the Terminal app (located in Applications > Utilities) and enter the command:
   ```sh
   xcode-select --install
   ```
   A pop-up window will prompt you to install the Command Line Tools. Click "Install" to proceed. After installation is complete, move on to the next step.

## Step 1: Install Homebrew

With the Xcode Command Line Tools installed, you can now install Homebrew. Homebrew is a package manager for macOS that simplifies the installation of software packages like PostgreSQL.

After installing Homebrew, it’s important to add it to your system’s PATH. This tells the system where to find the Homebrew executables, allowing you to run Homebrew commands from any location in your Terminal.

**1. Install Homebrew**
Copy and paste the following command into the Terminal app. The script will automatically download and install Homebrew on your Mac. You might be asked to enter your admin password during the installation process.
   ```sh
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
   After the installation, you will see a message saying, "Installation successful!"

**2. Add Homebrew to Your PATH**
To complete the installation, add Homebrew to your PATH:
   ```sh
   (echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> /Users/your_username/.zprofile
   ```
   Replace `/Users/your_username` with your actual user directory.

**3. Load Homebrew Environment Variables**
Run the following command to load the Homebrew environment variables into your current Terminal session:
   ```sh
   eval "$(/opt/homebrew/bin/brew shellenv)"
   ```

**4. Verify the Installation**
To confirm Homebrew is installed correctly, run:
   ```sh
   brew --version
   ```
   This should display the Homebrew version number.

## Step 2: Install PostgreSQL

In this step, you will use Homebrew to install PostgreSQL on your macOS system.

**1. Ensure Homebrew is Installed**
Make sure you have Homebrew installed. If not, refer to the previous section to install it.

**2. Update Homebrew**
Update Homebrew to ensure you have the latest package information:
   ```sh
   brew update
   ```

**3. Install PostgreSQL 14**
Install PostgreSQL 14 using Homebrew:
   ```sh
   brew install postgresql@14
   ```

**4. Start PostgreSQL Service**
After installation, start the PostgreSQL service:
   ```sh
   brew services start postgresql@14
   ```
   You should see a message indicating that PostgreSQL has started successfully.

**5. Verify PostgreSQL Installation**
Check the PostgreSQL version to ensure it’s installed correctly:
   ```sh
   psql --version
   ```

**6. Create a PostgreSQL User**
Create a new PostgreSQL user named `postgres` with superuser privileges:
   ```sh
   createuser -s postgres
   ```

**7. Set a Password for the `postgres` User**
Set a password for the `postgres` user:
   ```sh
   psql
   \password postgres
   ```

**8. Configure PostgreSQL Environment**
Add PostgreSQL to your PATH by adding the following line to your shell profile (`~/.zshrc` or `~/.bash_profile`):
   ```sh
   export PATH="/usr/local/opt/postgresql@14/bin:$PATH"
   ```
   Then, reload your profile:
   ```sh
   source ~/.zshrc   # or source ~/.bash_profile
   ```

**9. Troubleshooting Tips**
If the PostgreSQL service does not start, check the logs for errors:
   ```sh
   tail -f /usr/local/var/log/postgres.log
   ```
   Ensure your system has enough resources and dependencies for PostgreSQL.

## Step 3: Download the Northwind PostgreSQL SQL File

The Northwind database is a sample database originally provided by Microsoft. It contains data on customers, orders, products, suppliers, and other aspects of a fictitious company named "Northwind Traders". We will use a version of Northwind adapted for PostgreSQL.

**1. Open Terminal**
**2. Create a New Directory**
Create a new directory for the Northwind database and navigate to it:
   ```sh
   mkdir northwind && cd northwind
   ```

**3. Download the SQL File**
Download the Northwind PostgreSQL SQL file using curl:
   ```sh
   curl -O https://raw.githubusercontent.com/pthom/northwind_psql/master/northwind.sql
   ```

## Step 4: Create a New PostgreSQL Database

Now that you have downloaded the Northwind SQL file, it’s time to create a new database on your PostgreSQL server.

**1. Connect to PostgreSQL Server**
Connect as the `postgres` user:
   ```sh
   psql -U postgres
   ```

**2. Create Database**
Create a new database called `northwind`:
   ```sql
   CREATE DATABASE northwind;
   ```

**3. Exit PostgreSQL Interface**
Exit the `psql` command-line interface:
   ```sql
   \q
   ```

## Step 5: Import the Northwind SQL File

Import the Northwind SQL file into the `northwind` database.

**1. Ensure You’re in the Correct Directory**
Ensure you’re in the `northwind` directory where the `northwind.sql` file is located.

**2. Import the SQL File**
Run the following command to import the Northwind SQL file into the `northwind` database:
   ```sh
   psql -U postgres -d northwind -f northwind.sql
   ```

## Step 6: Verify the Northwind Database Installation

Verify that the Northwind database has been installed correctly.

**1. Connect to the `northwind` Database**
Connect using `psql`:
   ```sh
   psql -U postgres -d northwind
   ```

**2. List Tables**
List the tables in the Northwind database:
   ```sql
   \dt
   ```
   You should see a list of Northwind tables.

**3. Run a Sample Query**
Query the `customers` table to ensure data has been imported correctly:
   ```sql
   SELECT * FROM customers LIMIT 5;
   ```

**4. Exit the `psql` Interface**
Exit the command-line interface:
   ```sql
   \q
   ```

Congratulations! You have successfully installed the Northwind database in PostgreSQL using an SQL file and `psql`.

## Step 7: Connect to the Database Using Jupyter Notebook

Jupyter Notebook is a great tool for executing SQL queries and analyzing the Northwind database.

**1. Install ipython-sql**
Install the `ipython-sql` package:
   ```sh
   !pip install ipython-sql
   ```

**2. Load SQL Extension**
Load the SQL extension:
   ```python
   %load_ext sql
   ```

**3. Connect to the Northwind Database**
Establish a connection:
   ```python
   %sql postgresql://postgres@localhost:5432/northwind
   ```

   On Windows, you may need to include the password:
   ```python
   %sql postgresql://postgres:{password}@localhost:5432/northwind
   ```

**4. Run the Cell**
Run the cell by either clicking the "Run" button or using the keyboard shortcut `Shift + Enter` or `Ctrl + Enter`.

**5. Verify Connection**
You should see an output confirming the connection:
   ```text
   'Connected: postgres@northwind'
   ```

## Next Steps

Based on what you’ve accomplished, here are some next steps to continue your learning journey:

1. **Deepen Your SQL Knowledge:**
   - Formulate more complex queries on the Northwind database.
   - Understand the design of the Northwind database.

2. **Experiment with Database Management:**
   - Learn how to backup and restore databases in PostgreSQL.
   - Explore ways to optimize your PostgreSQL database performance.

3. **Integration with Python:**
   - Use `psycopg2`, a popular PostgreSQL adapter for Python.
   - Experiment with ORM libraries like `SQLAlchemy` to manage your database using Python.

4. **Security and Best Practices:**
   - Learn about database security principles and apply them to your PostgreSQL setup.
   - Understand best practices for storing sensitive information.

---

This blog post provides a comprehensive guide to installing PostgreSQL 14.7 on macOS using Homebrew, importing the Northwind database, and connecting to it using Jupyter Notebook.

## Further reading

- Read [about reference](https://diataxis.fr/reference/) in the Diátaxis framework
