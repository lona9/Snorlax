CREATE TABLE IF NOT EXISTS reminders (
  ReminderID NUMERIC PRIMARY KEY,
  ReminderTime DATE,
  ReminderText VARCHAR,
  ReminderAuthor VARCHAR,
  ReminderChannel NUMERIC
);

CREATE TABLE IF NOT EXISTS tasks (
  TaskID VARCHAR PRIMARY KEY,
  TaskText VARCHAR,
  TaskStatus VARCHAR,
  TaskCategory VARCHAR DEFAULT "Unsorted"
);
