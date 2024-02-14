## API-Dev-Exercise project. Further details are found in README.md in the respective Tasks.

Reflections from code review: Task 1: Was 2 collections necessary?

how to do it without Mongo aggregation pipeline? DB is being taxed, it could be done in memory(python code)

All ids in 1 document.  can compile before inserting. Have 1 document for each ID. Personally don't find this good, because then you are modifying the information you are given, not doing operations on them. original documents should probably not be changed at first.

How debug aggregation pipeline? => did with Mongo


Testing: Each pipeline split into its own function, then output be tested on a unit level without db mock.

Log file instead of prints? or debugging would be better.

Task2