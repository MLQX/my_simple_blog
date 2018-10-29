drop table if exists entries;

create table entries(
  [id] integer primary key autoincrement,
  [title] string not null unique,
  [content] TEXT not null,
  [createtime] TimeStamp NOT NULL DEFAULT (datetime('now','localtime'))
);

