# How to Contribute to this Project

Generally, this project follows a pretty standard GitHub workflow: If you make a
change, submit a pull request, and we'll review it. If we ask you to change
something, please do so. If you submit a PR, it is your responsibility to
contribute to it until it gets closed. Also, please, please PLEASE search for
duplicate pull requests/issues *before* you submit a new one! It makes
everyone's life, including yours, a whole lot easier.

## Getting Started

For more detailed instructions on how to get started, please see [this wiki
page.](https://github.com/djpetti/grobot/wiki/Getting-Started)

## Styleguides

We do believe in styleguides around here. We suggest that you familiarize
yourself with them before contributing. Code that does not follow the
styleguide will not be merged.

We use the Google styleguides for everything, pretty much. You can find
links below.

- [Google Python Styleguide](https://google.github.io/styleguide/pyguide.html)
- [Google C++ Styleguide](https://google.github.io/styleguide/cppguide.html)
- [Google JavaScript Styleguide](https://google.github.io/styleguide/javascriptguide.xml)

The code on the MCU is written in C, which Google (to my knowledge) does not
have a styleguide for. Therefore, we follow the C++ styleguide mostly, and just
ignore the parts pertaining to C++-only features. Furthermore, we also write our
C function names lowercase\_with\_underscores, as this matches better with
existing C naming paradigms.

Also, for JS code, we are not (yet) requiring you to use the Closure compiler,
although this will be changing in the future.
