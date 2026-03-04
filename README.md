# 🗳️ Terminal-Based Electronic Voting System

A robust, object-oriented Python application that simulates a real-world electronic voting environment. This system is designed with a strong focus on separation of concerns, data persistence, and fraud prevention, making it a reliable backend prototype for electoral processes.

## 🌟 Key Features

* **Dual-Interface Architecture:** Separate Command Line Interfaces (CLI) for the Polling Station President (Admin) and the general public (Voters).
* **Inter-Process Communication (IPC):** The Admin terminal can remotely lock and shut down the public Voter terminal in real-time using a flag-file system (`urnas_fechadas.flag`).
* **Strict Fraud Prevention:** * Validates Voter ID (CC) against an authorized census database (`recenseamento.csv`).
    * Prevents duplicate voting by tracking realtime attendance (`caderneta.csv`).
* **Data Persistence:** Uses the `pandas` library to read and save voting states instantly to CSV files, ensuring zero data loss even if the system is abruptly closed.
* **Comprehensive Voting Logic:** Accurately processes and tallies valid candidate votes, blank votes, and null votes.

## 🛠️ Tech Stack

* **Language:** Python 3
* **Data Manipulation:** Pandas
* **Storage:** CSV (Comma-Separated Values)
* **Architecture:** Object-Oriented Programming (OOP), Modular Design

## 📁 Project Structure

* `backend.py`: The core engine containing the business logic and class definitions (`Urna`, `Caderneta`, `Recenseamento`, `Pessoa`, `Candidato`).
* `interface_eleitor.py`: The public-facing terminal for voters to cast their ballots.
* `interface_admin.py`: The control panel for the Polling Station President to monitor results and close the polls.
* `*.csv`: Database files used for persistence (Census, Attendance, and Results).

## 🚀 How to Run

### Prerequisites
Make sure you have Python installed, along with the `pandas` library:
```bash
pip install pandas

```
## Execution
* To fully experience the system, it is recommended to open two separate terminal windows:
* **1. Start the Admin Panel:**
In the first terminal run:
```bash
python interface_admin.py
```
* **2. Start the Voter Terminal:**
In the second terminal run:
```bash
python interface_eleitor.py
```
* 3. Test the IPC:** Try casting a vote in the Voter terminal. Then, use the "Close Polls" option in the Admin terminal and watch the Voter terminal automatically shut down.

## Future Enhancements (Roadmap)
* [  ] Add timestamp logging for voting audits.
* [  ] Implement password hashing for Admin access.
* [  ] Develop a Graphical User Interface (GUI) to replace the CLI.