# Method3 DesignPlan

## 实验分析

根据题目所给出的文法构造相应的拓广文法，并求出该文法各非终结符的FIRST、FOLLOW集合；构造拓广文法的项目集规范族，并构造出识别所有前缀的DFA；构造文法的LR分析表；由此构造LR分析程序。

## 设计文法

（1）S→E

（2）E→E+T

（3）E→E-T

（4）E→T

（5）T→T*F

（6）T→T/F

（7）T→F

（8）F→(E)

（9）F→num

## 构造识别改文法所有活前缀的DFA
![Alt text](https://github.com/FGinfinite/CompilationLab/blob/8a9313cdc43751acaebfe4011d25257b4b65b7af/Lab2/Lab2Method3/imgs/DFA.png)
## LR分析表
![Alt text](https://github.com/FGinfinite/CompilationLab/blob/81d44f878bc32afda117c04a438f4e446865ba18/Lab2/Lab2Method3/imgs/Table.png)
