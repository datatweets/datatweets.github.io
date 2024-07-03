---
layout: post
title:  "Install PostgreSQL 14.7 on Windows 10"
date:   2024-07-02 19:54:02 +0430
categories: jekyll update
---

## Introduction

In this tutorial, you'll learn how to install PostgreSQL 14.7 on Windows 10.

The process is straightforward and consists of the following steps:

1. Install PostgreSQL
2. Configure Environment Variables
3. Verify the Installation
4. Download the Northwind PostgreSQL SQL file
5. Create a New PostgreSQL Database
6. Import the Northwind SQL file
7. Verify the Northwind database installation
8. Connect to the Database Using Jupyter Notebook

## Prerequisites

- A computer running Windows 10
- Internet connection

1. Download the official PostgreSQL 14.7 at [https://get.enterprisedb.com/postgresql/postgresql-14.7-2-windows-x64.exe](https://get.enterprisedb.com/postgresql/postgresql-14.7-2-windows-x64.exe)
2. Save the installer executable to your computer and run the installer.

*Note: We recommend version 14.7 because it is commonly used. There are newer versions available, but their features vary substantially!*

## Step 1: Install PostgreSQL

We're about to initiate a vital part of this project - installing and configuring PostgreSQL.

Throughout this process, you'll define critical settings like the installation directory, components, data directory, and the initial 'postgres' user password. This password grants administrative access to your PostgreSQL system. Additionally, you'll choose the default port for connections and the database cluster locale.

Each choice affects your system's operation, file storage, available tools, and security. We're here to guide you through each decision to ensure optimal system functioning.

1. In the PostgreSQL Setup Wizard, click **Next** to begin the installation process.

![Step 1](https://i.ibb.co/p3QdCBR/01.png)

2. Accept the default installation directory or choose a different directory by clicking **Browse**. Click **Next** to continue.

![Step 2](https://i.ibb.co/G7tPYXq/02.png)

3. Choose the components you want to install (e.g., PostgreSQL Server, pgAdmin 4 (optional), Stack Builder (optional), Command Line Tools),no characters will appear on the screen as you type your password and click **Next**.

![Step 3](https://i.ibb.co/nmpf7CK/03.png)

4. Select the data directory for storing your databases and click **Next**.

![Step 4](https://i.ibb.co/NtWyjhP/04.png)

5. Set a password for the PostgreSQL “postgres” user and click **Next**.

![Step 5](https://i.ibb.co/R7pZzqH/05.png)

- There will be some points where you're asked to enter a password in the command prompt. It's important to note that for security reasons, as you type your password, no characters will appear on the screen. This standard security feature is designed to prevent anyone from looking over your shoulder and seeing your password. So, when you're prompted for your password, don't be alarmed if you don't see any response on the screen as you type. Enter your password and press 'Enter'. Most systems will allow you to re-enter the password if you make a mistake.
- **Remember, it's crucial to remember the password you set during the installation, as you'll need it to connect to your PostgreSQL databases in the future.**

6. Choose the default port number (5432) or specify a different port, then click **Next**.

![Step 6](https://i.ibb.co/RB45WVZ/06.png)

7. Select the locale to be used by the new database cluster and click **Next**.

![Step 7](https://i.ibb.co/TrDrZcq/07.png)

8. Review the installation settings and click **Next** to start the installation process. The installation may take a few minutes.

![Step 8](https://i.ibb.co/S65bfCk/08.pngz)
![Step 9](https://i.ibb.co/R2PqTr4/09.png)

9. Once the installation is complete, click **Finish** to close the Setup Wizard.

## Step 2: Configure Environment Variables

Next, we're going to configure **environment variables** on your Windows system. Why are we doing this? Well, environment variables are a powerful feature of operating systems that allow us to specify values - like directory locations - that can be used by multiple applications. In our case, we need to ensure that our system can locate the PostgreSQL executable files stored in the "bin" folder of the PostgreSQL directory.

By adding the PostgreSQL "bin" folder path to the system's PATH environment variable, we're telling our operating system where to find these executables. This means you'll be able to run PostgreSQL commands directly from the command line, no matter what directory you're in, because the system will know where to find the necessary files. This makes working with PostgreSQL more convenient and opens up the possibility of running scripts that interact with PostgreSQL.

Now, let's get started with the steps to configure your environment variables on Windows!

1. On the **Windows taskbar**, right-click the **Windows** icon and select **System**.
2. Click on **Advanced system settings** in the left pane.
3. In the **System Properties** dialog, click on the **Environment Variables** button.

![Environment Variables](https://i.ibb.co/YTVfGBN/10.png)

4. Under the **System Variables** section, scroll down and find the **Path** variable. Click on it to select it, then click the **Edit** button.
5. In the **Edit environment variable** dialog, click the **New** button and add the path to the PostgreSQL **bin** folder, typically `C:\Program Files\PostgreSQL\14\bin`.

![Edit Environment Variables](https://i.ibb.co/GFxpVg7/12.png)

6. Click **OK** to close the **"Edit environment variable"** dialog, then click **OK** again to close the **"Environment Variables"** dialog, and finally click **OK** to close the **"System Properties"** dialog.

## Step 3: Verify the Installation

After going through the installation and configuration process, it's essential to verify that PostgreSQL is correctly installed and accessible. This gives us the assurance that the software is properly set up and ready to use, which can save us from troubleshooting issues later when we start interacting with databases.

If something went wrong during installation, this verification process will help you spot the problem early before creating or managing databases.

Now, let's go through the steps to verify your PostgreSQL installation.

1. Open the Command Prompt by pressing Win + R, typing **cmd,** and pressing **Enter**.
2. Type `psql --version` and press **Enter**. You should see the PostgreSQL version number you installed if the installation was successful.
3. To connect to the PostgreSQL server, type `psql -U postgres` and press **Enter**.
4. When prompted, enter the password you set for the **postgres** user during installation. You should now see the `postgres=#` prompt, indicating you are connected to the PostgreSQL server.

## Step 4: Download the Northwind PostgreSQL SQL File

Now, we're going to introduce you to the Northwind database and help you download it. The Northwind database is a sample database originally provided by Microsoft for its Access Database Management System. It's based on a fictitious company named "Northwind Traders," and it contains data on their customers, orders, products, suppliers, and other aspects of the business. In our case, we'll be working with a version of Northwind that has been adapted for PostgreSQL.

The following steps will guide you on how to download this PostgreSQL-compatible version of the Northwind database from GitHub to your local machine. Let's get started:

First, you need to download a version of the Northwind database that's compatible with PostgreSQL. You can find [an adapted version on GitHub](https://github.com/pthom/northwind_psql/tree/master). To download the SQL file, follow these steps:

1. Open your Terminal application.
2. Create a new directory for the Northwind database and navigate to it:

   ```bash
   mkdir northwind && cd northwind
   ```

3. Download the Northwind PostgreSQL SQL file using curl:

   ```bash
   curl -O https://raw.githubusercontent.com/pthom/northwind_psql/master/northwind.sql
   ```

   This will download the `northwind.sql` file to the `northwind` directory you created.

## Step 5: Create a New PostgreSQL Database

Now that we've downloaded the Northwind SQL file, it's time to prepare our PostgreSQL server to host this data. The next steps will guide you in creating a new database on your PostgreSQL server, a crucial prerequisite before importing the Northwind SQL file.
## Step 5: Create a New PostgreSQL Database (continued)

Creating a dedicated database for the Northwind data is good practice as it isolates these data from other databases in your PostgreSQL server, facilitating better organization and management of your data. These steps involve connecting to the PostgreSQL server as the `postgres` user, creating the `northwind` database, and then exiting the PostgreSQL command-line interface.

Let's proceed with creating your new database:

1. Connect to the PostgreSQL server as the `postgres` user:
   
   ```bash
   psql -U postgres
   ```

2. Create a new database called `northwind`:
   
   ```sql
   CREATE DATABASE northwind;
   ```

3. Exit the `psql` command-line interface:
   
   ```sql
   \q
   ```

## Step 6: Import the Northwind SQL File

We're now ready to import the Northwind SQL file into our newly created `northwind` database. This step is crucial as it populates our database with the data from the Northwind SQL file, which we will use for our PostgreSQL learning journey.

These instructions guide you through the process of ensuring you're in the correct directory in your Terminal and executing the command to import the SQL file. This command will connect to the PostgreSQL server, target the `northwind` database, and run the SQL commands contained in the `northwind.sql` file.

Let's move ahead and breathe life into our `northwind` database with the data it needs!

With the `northwind` database created, you can import the Northwind SQL file using `psql`. Follow these steps:

1. In your Terminal, ensure you're in the `northwind` directory where you downloaded the `northwind.sql` file.
2. Run the following command to import the Northwind SQL file into the `northwind` database:
   
   ```bash
   psql -U postgres -d northwind -f northwind.sql
   ```

   This command connects to the PostgreSQL server as the `postgres` user, selects the `northwind` database, and executes the SQL commands in the `northwind.sql` file.

## Step 7: Verify the Northwind Database Installation

You've successfully created your `northwind` database and imported the Northwind SQL file. Next, we must ensure everything was installed correctly, and our database is ready for use.

These upcoming steps will guide you on connecting to your `northwind` database, listing its tables, running a sample query, and finally, exiting the command-line interface. Checking the tables and running a sample query will give you a sneak peek into the data you now have and verify that the data was imported correctly. This means we can ensure everything is in order before diving into more complex operations and analyses.

To verify that the Northwind database has been installed correctly, follow these steps:

1. Connect to the `northwind` database using `psql`:
   
   ```bash
   psql -U postgres -d northwind
   ```

2. List the tables in the Northwind database:
   
   ```sql
   \dt
   ```

   You should see a list of Northwind tables: categories, customers, employees, orders, and more.

3. Run a sample query to ensure the data has been imported correctly. For example, you can query the `customers` table:
   
   ```sql
   SELECT * FROM customers LIMIT 5;
   ```

   This should return the first five rows from the `customers` table.

4. Exit the `psql` command-line interface:
   
   ```sql
   \q
   ```

Congratulations! You've successfully installed the Northwind database in PostgreSQL using an SQL file and `psql`.

## Step 8: Connect to the Database Using Jupyter Notebook

As we wrap up our installation, we will now introduce Jupyter Notebook as one of the tools available for executing SQL queries and analyzing the Northwind database. Jupyter Notebook offers a convenient and interactive platform that simplifies the visualization and sharing of query results, but it's important to note that it is an optional step. You can also access Postgres through other means. However, we highly recommend using Jupyter Notebook for its numerous benefits and enhanced user experience.

To set up the necessary tools and establish a connection to the Northwind database, here is an overview of what each step will do:

1. `!pip install ipython-sql`: This command installs the `ipython-sql` package. This package enables you to write SQL queries directly in your Jupyter Notebook, making it easier to execute and visualize the results of your queries within the notebook environment.

2. `%sql postgresql://postgres@localhost:5432/northwind`: This command establishes a connection to the Northwind database using the PostgreSQL database system. The connection string has the following format:

   ```python
   postgresql://username@hostname:port/database_name
   ```

   In this case, `username` is `postgres`, `hostname` is `localhost`, `port` is `5432`, and `database_name` is `northwind`. The `%sql` magic command allows you to run a single-line SQL query in the Jupyter Notebook.

3. Copy the following text into a code cell in the Jupyter Notebook:

   ```python
   !pip install ipython-sql
   %load_ext sql
   %sql postgresql://postgres@localhost:5432/northwind
   ```

   On Windows you may need to try the following command because you need to provide the password you set for the “postgres” user during installation:

   ```python
   %sql postgresql://postgres:{password}@localhost:5432/northwind
   ```

   Bear in mind that it's considered best practice **not to include sensitive information like passwords directly in files that could be shared or accidentally exposed**. Instead, you can store your password securely using environment variables or a password management system (we'll link to some resources at the end of this guide if you are interested in doing this).

4. Run the cell by either:
   - Clicking the "Run" button on the menu bar.
   - Using the keyboard shortcut: `Shift + Enter` or `Ctrl + Enter`.

5. Upon successful connection, you should see an output similar to the following:

   ```text
   'Connected: postgres@northwind'
   ```

   This output confirms that you are now connected to the Northwind database, and you can proceed with the guided project in your Jupyter Notebook environment.

Once you execute these commands, you'll be connected to the Northwind database, and you can start writing SQL queries in your Jupyter Notebook using the `%sql` or `%%sql` magic commands.

## Next Steps

Based on what you've accomplished, here are some potential next steps to continue your learning journey:

1. **Deepen Your SQL Knowledge:**
   - Try formulating more complex queries on the Northwind database to improve your SQL skills. These could include joins, subqueries, and aggregations.
   - Understand the design of the Northwind database: inspect the tables, their relationships, and how data is structured.

2. **Experiment with Database Management:**
   - Learn how to backup and restore databases in PostgreSQL. Try creating a backup of your Northwind database.
   - Explore different ways to optimize your PostgreSQL database performance like indexing and query optimization.

3. **Integration with Python:**
   - Learn how to use `psycopg2`, a popular PostgreSQL adapter for Python, to interact with your database programmatically.
   - Experiment with ORM (Object-Relational Mapping) libraries like `SQLAlchemy` to manage your database using Python.

4. **Security and Best Practices:**
   - Learn about database security principles and apply them to your PostgreSQL setup.
   - Understand best practices for storing sensitive information, like using `.env` files for environment variables.
   - For more guidance on securely storing passwords, you might find the following resources helpful:
     - [Using Environment Variables in Python](https://dev.to/aligoren/using-environment-variables-in-python-3ofm)
     - [Python Secret Module](https://pypi.org/project/python-decouple/)
