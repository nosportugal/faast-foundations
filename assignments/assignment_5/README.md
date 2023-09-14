# Assignment 5: Design Patterns

The focus of this (final) assignment is about OOP and design patterns. And we have bad news: we went to check the Eurostat source and now they are using JSON as a data format. Also, the file was zipped.

> Don't forget to create a branch for this assignment.

## 1- Design Patterns

1. Copy the JSON data from the `assignment_4` folder to the `life_expectancy/data` folder.
2. Refactor your code so that it can accept and clean data in other formats if necessary. You can use the [Strategy pattern](https://refactoring.guru/design-patterns/strategy) for this, but you can also use a different one if you prefer.
3. Create the new tests for your solution. Don't forget to run an end-to-end test for the pipeline using JSON data.
4. Ensure you still have complete test coverage and a high `pylint` score.

## 2- Enums

Ok, the final stretch. You can do this. Passing a country as a string is not very safe (imprecise types are a code smell). We can use an enum to make sure that we only pass valid countries.

1. Create an `enum.Enum` called `Region` with possible country or region values.
2. Then, modify the necessary functions and tests to accept a `Region` instead of a string. Don't forget the type hints.
3. Finally, add a class method to `Region` that returns a list of all the _actual_ countries (so, it removes values like EU28, EFTA, etc). Add a test for this method.

## 3- Code Review

As with the previous assignment, a peer should review your code and you will be reviewing the code of a fellow colleague.

Was your PR approved? Great! Now you can merge it into `main`, submit the assignment and go celebrate! 🎈
