create table entries (
  id integer primary key autoincrement,
  stdnum text unique,
  name text not null,
  sex text not null,
  email text not null,
  phone text not null,
  info text not null
);