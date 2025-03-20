OPENQASM 2.0;
include "qelib1.inc";

qreg q[4];
creg c[4];
x q[1];
cx q[2], q[3];
h q[0];
swap q[1], q[2];
tdg q[3];
s q[0];
z q[1];
p(pi/2) q[2];

measure q -> c;