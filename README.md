#GroBot
Software for the GroBot project.

#How to Use this Project

##Running Code Locally

Some of the GroBot code does not require specific hardware, and can be run on
your laptop. This includes the web interface. To test it, you currently have to
be on the "web" branch. After that, you can run

```
python/server.py
```

It is important that you run it from the main directory.

After you do this, the content will be served on port 8080.

##Unit Testing

Currently, unit tests exist for the web interface backend. The unit tests must
pass before anything can be merged. You can run them like so:

```
python/run_tests.py
```

(Note that, in this case, you can run the tests from any directory.)
