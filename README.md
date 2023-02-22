# Bank management system using Python and SQLite3

## Objective
- Build a **Bank Management System** (`BMS`) that connects to a `sqlite3` database.
- The `BSM` should allow a customer to : `open` new account, `check` balance, `deposit` funds, `withdraw` funds,  `delete` their account, and `exit` from the program.
- Become familiar with `SQL`, and `CRUD` operations.

## Screenshots 

![image](https://user-images.githubusercontent.com/72005563/220712796-a7cafd62-0da3-4f64-8c7e-aec9e5aed18f.png)


![image](https://user-images.githubusercontent.com/72005563/220711569-dab09b0a-cdd7-4b92-8092-05aba05749ff.png)
![image](https://user-images.githubusercontent.com/72005563/220711799-5870d4b2-386e-488d-86ab-e48d4da16996.png)



## class: BMSConnection (Database)

### Attributes
- `conn` - **filename**: `transactions.db`
- `curr` - _The connection cursor_

### Methods

- `create_customer_table`
- `create_transaction_table`
- `save_to_customer_tb`
- `save_to_transaction_tb`


## class: BMSApplication



### Attributes
- `connection` - `BMSConnection` class  

### Methods

- `open_account`
- `deposit_funds`
- `withdraw_funds`
- `check_balance`
- `delete_account`


###  Customer table

| Fields       | Data Type           |
|--------------|---------------------|
| `id`         | Int (_primary key_) |
| `first_name` | Text                |
| `last_name`  | Text                |

### Transactions table


| Fields             | Data Type           |
|--------------------|---------------------|
| `id`               | Int (_primary key_) |
| `customer_id`      | Int (_foreign key_) |
| `account_number`   | Text                |
| `username`         | Text                |
| `pin`              | Text                |
| `transaction_date` | Text                |
| `ledger`           | Text                |
| `balance`          | Real                |

