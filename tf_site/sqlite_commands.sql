-- SQLite
select * from sqlite_sequence;

-- Resets pk:id field to 0; used when unloading table;
update sqlite_sequence set seq = 0 where name = 'iris_iris';


select 
    classification
,   count(*)
,   avg(petal_length)

from iris_iris
group by 
    classification
