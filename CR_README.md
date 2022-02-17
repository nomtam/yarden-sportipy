# \[MD\] General notes

## Large design / collective CR comments

1. Data models relations
* Almost all of the models have a bidirectional relationship.
For example, each song have the artists that created it and the album it is in.
Yet each album has the songs in it.
And each artist has both the albums they created and the songs they created (that can already be referenced from their albums).

[MIKI - I DON'T KNOW WHAT THE EXERCISE HAS ASKED, CONFIRM OR DELETE IF IRRELEVANT, BUT - DATA RELATIONS DEFINITIONS ARE DEPENDANT ON WHAT THE REQUESTED FEATURES ARE. FOR INSTNACE, IF ALBUMS ARE USED SOLELY FOR SEARCH, THE FOLLOWING EXAMPLE WOULD BE GOOD]
While it might be comfortable to work with bidirectional relations in this scope, it might be an unnecessary duplication of data, which is more critical in real life use cases.
For example, if albums are mere names to group songs by - we don't need to have them reference to any song.
Each songs is defined it's album and each artist is defined their songs. An album would only contains it's name and the artists who created it.


* The `Song` class -
    - How come `Song` class has `artistS` proeprty but not `Album`? Can't two artists work on an album?
    - Can't a song be a single? I.E. not part of an album?

2. Avoid using generic wording when naming variables or functions.
collection_objects -> collections
json_docs -> documents
create_song_obj -> create_song

3. Type hint everything. It makes everything so much more readable.
It's a _must_ when working on a non-script python code base.

4. It's advisable to have the entry point of your application at the root of the project, and the whole "code" sections in an 'src' or 'APP_NAME' (sportipy here)
- Easier imports and clear relations between the modules (i.e. your config.py won't have path backtracking)
- It's visibly clearer where the entry point is (I usually expect core to contain inside-use modules and / or common models)
...to name a few

5. Skip old-python / C style templating ('%s' % (v1, v2, v3)) and use `.format` or f'string styles.

## If you have some extra time

* Are you familiar with the concept of **ORM**?
Using ORM can help unify the implementation, serialization / deserialization and retrieval of every data model in your code base.
For example, you could (disregarding whether it's the best option for this use-case or not) create a `SportipyModelBase` class
that requires a `Collection` Type / `collection_name: str`. That way you won't have to pass the collection name every time you want to save an object,
as the DAL interface will be able select the correct collection using the model itself.

Moreover, it allows better DI (DAL interface accepts a unified type, and calls `serialize()` defined at the base class / overridden by children)

* Consider using a configuration module / library instead having a bunch of strings in a python file. That way you'll have:
    - The ability to differ values between environments (prod / test / dev)
    - Being able to override values in different ways (i.e. environment variables in deployment environment)
    - Serialize and save the configuration in a "configuration" type scheme (json, yaml, toml)
    - You wouldn't have to commit and push changes each time you want a value changed

* Are you familiar with the `abc` builtin module? It helps create and enforce abstract classes / methods.
You could try using it in places where you want to perform DI.


## Things to Preserve
* Using `logging` instead of mere `print` statements
* Type Hints! - Althought not all of the code was covered, great job on using typings.
They help a ton when working / reading someone elses code, without much effort \.
* 
