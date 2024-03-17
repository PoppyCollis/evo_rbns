
Developing automated procedures for the design of networks is an appealing goal for
complexity science, both from an engineering standpoint and with a view of gaining insight
into living systems. As highly abstracted model systems, Boolean networks (BNs) have been
shown to capture the fundamental principles underlying the dynamics of real biological
networks surprisingly well. Through the implementation of self-loops in node connections,
BNs can be made to model a subtle computational property of networks known as direct
autoregulation, giving rise to more robust attractor dynamics under certain conditions
(Montagna et al., 2021). While previous research has been conducted into the automated
design of BNs through stochastic search techniques (Roli et al., 2009; 2011), the impact of
self-loops on our ability to design BNs is yet to be investigated. In this study, we present a
method to design BNs to have specific predefined attractor lengths using a genetic algorithm
(GA), and investigate the effect that self-loops have on the success of this task. We found
that we were able to successfully design BNs both with and without self-loops but that
increasing the ratio of self-loops within the network reduced the performance of the design
procedure. Our results have implications for evolutionary robotics and the use of BNs in
automated control systems.

<strong>INSTRUCTIONS FOR RUNNING THE CODE</strong>

Run network.py to perform a single trial of 15 independent evolutionary runs (this number can be changed via the 'runs' varibale in the main function. Set the desired network and GA parameters at the top of the code and make sure than these values are matched in the main function when it instantiates an object of the Population class.

To test without the presence of self-loops, set the Population object variable 'self_inputs' to False. 
To test the presence of self-loops occurring at random (i.e. 15%) set the variable to True. 
To change the ratio of nodes with self-inputs, uncomment lines 58 - 61 in Population.py and set the variable 'sl_ratio' to the desired amount. Then in Network.py, set the value of self_inputs to be False when calling it. Although False, uncommenting the lines will then adjust the ratio and allow self-inputs.
