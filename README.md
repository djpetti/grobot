# What is GroBot?

GroBot is an open-source, modular hydroponics system. A GroBot system consists of a vertical stack of **grow modules**, which contain plants, as well as LED lighting fixtures. A complete system also has a **base module**, a single unit which provides power and water to an entire stack of **grow modules**.

GroBot is designed to be flexible and highly automated. Each unit contains a myriad of sensors for measuring such things as water quality, ambient conditions, and lighting output. Furthermore, the entire system is monitored and administered via a web interface.

![GroBot CAD](https://rcos.io/uploads/djpetti/grobot/v2RXgdI20yYIzJiS_SVfr5oc.png)

GroBot is currently affiliated with the [Rensselaer Center for Open Source](https://rcos.io/).

# Why Grobot?

GroBot is designed to provide various advantages over existing systems, which include

- Lower cost.
- Modularity, expandability and customization.
- Simple, web-based UI.
- High level of automation.
- Open source.

# How does it Work?

GroBot is a vertical drip hydroponics system. That means that it delivers nutrients to plants by pumping water up to the top of the stack, and letting it trickle down, through the plant growing medium, and back into the reservoir.

Internally, GroBot uses a [PSoC 4](http://www.cypress.com/documentation/datasheets/psoc-4-psoc-4200-family-datasheet-programmable-system-chip-0) microcontroller in every module. (Although we are transitioning away from that, see the [hardware page](https://github.com/djpetti/grobot/wiki/Hardware) for details.) The base module also includes a [CHIP SBC](https://getchip.com/pages/chip), which is tasked mainly with serving the web interface.

Most low-level functionality is handled by the MCUs, which are programmed in C. The web interface stack includes [Tornado](https://github.com/tornadoweb/tornado/tree/stable) on the backend, and [Polymer](https://www.polymer-project.org/1.0/) on the frontend.

# How can I Help?

The system is currently under heavy development. The hardware is still very much in a prototype phase, and the software being actively created. We appreciate any contributions, particularly on the software side. If you have questions, or want to know something specific, feel free to contact me at [djpetti@gmail.com](mailto:djpetti@gmail.com)

The [issues](https://github.com/djpetti/grobot/issues) page currently has a list
of tasks which I have singled out as being something that interested people can
work on. Please check out the [contributing guidelines](https://github.com/djpetti/grobot/blob/master/CONTRIBUTING.md)
before you dive in.

For more detailed instructions and help getting started, please see [this wiki
page](https://github.com/djpetti/grobot/wiki/Getting-Started)
