drop table if exists switch;
create table switch (
  switch_id integer primary key autoincrement,
  output_id integer not null,
  title text not null,
  description text not null,
  state integer not null
);