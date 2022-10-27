# Alternate Description of Signals and Slots

It is essential to understand PySide6 signals and slots,  
for proper development of PySide6 projects.  
You need to know what they are,  how and why they should be used.

The first step to understanding, of course, is (re)reading the official documentation  

https://doc.qt.io/qtforpython/tutorials/basictutorial/signals_and_slots.html#signals-and-slots

Unfortunately,  the C++ (vs Python) oriented documentation left me still confused about the what, how and why.

After further research and playing around with code,  
I have come to the following understanding,  
which I would like to share for comment.

## What

Signals class is made available in the QObject class and thus inherited/used by all QObject derived classes,  especially the QWidget classes.

Signals are not mysterious,  they simply inherit,  as with all class instances,  
a number of properties and functions from their parent class Signals.

Signals are special however,  in the sense that they are always created in the top level namespace of a project (global scope)
  
### Signal properties include variables for:

- a connections list  
  
  A list of zero or more function addresses (call backs) to be run sequentially by a signal's `emit()` function - see below.  
  Functions in this list are called `slots` (rather than call-backs).  
  This list of slots is run-time managed using a signal's functions - see below.  
  Any function in a signal's scope can be a slot function (even other `signal.emit()` functions)

- an argument types list  
  
  A list of zero or more QObject derived types, corresponding to the number and types of arguments to be provided by the signal.  
  The argument type list is set permanently, when the signal is created.  

### Signal class functions include

- connect(fxn)  
  appends a given function (slot) to the connections list

- disconnect(fxn)  
  removes a given slot from the connections list

- disconnect()  
  removes ~all~ slots from the signal's connections list
  
- emit(*args)  
  This function is typically run by code (event handler) processing certain events in a project.  
  When `emit()` is run, each function that is currently in a signal's connections list will then also be run,  
  each with any arguments provided by `<signal>.emit(*args)`.

### About `arg*`

A signal's argument list is used in runtime,  to check if that the type and number of arguments in the `emit()` and `slot()` functions are equivalent.  

If not, the `signal.emit()` statement will be ignored and cause a runtime error.

Note:  

- the number of emitted arguments can be fewer without a runtime error,  
  if the slot function provides default values for the missing arguments
- there can be extra emit arguments, in which case the extra arguments will be ignored by the slot function
- the `QOject` type itself,  would allow ~any~ argument type to be accepted as an argument.
  
### Signals and Events confusion

Events and event handling are only available in QWidget based classes.  

Signals are QObject based and have nothing to do with events and handling events.  

However, `<object_name><signal_name>.emit(*args)`  statements frequently appear in event handler and event filter functions.  
Furthermore, a signal can have any arbitrary name,  but are often named similar to the associated event.  
Hence the initial confusion between `click`, a `Signal` object and `QMousePressEvent`, a `QEvent`.  

Thus,  when the literature loosely talks about a "signal event", "emitting a signal", "signal is emitted",  
what they mean is that when a certain event occurs,  an event handler runs a `<signal>.emit(*args)` statement for that event.  
If any slots are currently connected to the signal,  they will then be run directly with the arguments in `arg*`

### About @Slot(*args)

What and how decorator functions work,  like `@Slot()`, is a seperate topic,  
but in this case it is probably sufficient to understand that this optional decorator puts a link to the slot function in the project's global namespace.
This slot can now be connected to (called by) ~any~ project signal.
For example,  use a signal in one window,  to update widgets in another window.

### Summary

- The Signal class provides a function `emit(*args)` that makes it easier/safer to write code to dynamically run other function(s) in a project,  

- Signal emit statements are typically found in event handlers in a project's classes.

## How

The best way to really understand all the above,  is by actually doing it.  
Therefore,  open/read/run the following demos in a code editor,  
so you can read the comments and see the terminal output when run.  

### Example 1 - creating and using a signal

[new_signal_demo.py](new_signal_demo.py)  

### Example 2 - using an inherited signal

[title_signal_demo.py](title_signal_demo.py)

### About QMenu and QActions

Your first exposure to signals was probably coding `QMenu` instances,  
so it is worth reviewing what is happening with `QMmenu` and why understanding and using signals is essential.

An instance of `QMenu` exclusively manages a list of menu widgets,  their order and appearance.  
Each menu widget manages its own properties and any events that may occur in the widget.  
Since the corresponding code for creating a list of menu widgets is dynamic, complex and fragile (I suspect),  
almost all of it has been hidden by the designers of these classes.  
The event handlers in menu widgets, for example, cannot be subclassed in code.

Note: The only attributes that ~are~ exposed in menu widgets,  
are the attributes in the `QAction` object used by `QMenu` to create the menu widget.

Therefore, the best and only way to code responses to menu widget events,  
is to use the `connect()` functions of the inherited QAction `hovered` and `triggered` signals.

## Why

After all the above,  signals provide

- flexibile coding
  allowing events in one window,  to be easily make changes in one or more other windows

- safer coding
  by hiding blocks of complex code and using signals to expose only certain events,  
  that can be used in a project's code

- simpler, more readable coding
  since the event handlers and signals for many events have already been coded in classes,  
  using signals for a flexible coded response

- less buggy coding
  since there is automatic type and number checking of the emit() and slot() arguments
