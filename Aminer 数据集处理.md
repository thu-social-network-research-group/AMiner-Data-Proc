# Aminer 数据集处理

## Static following network

数据包含了在关注的时间段之前，用户的follow网络信息

涉及的文件为"weibo_network.txt"

文件格式如下：

- 第一行包含两个整数N和M，其中N代表用户的总人数，而M代表了关注边的数量。

  在接下来的N行中，每一行的起始两个数字分别为 v1_id, k; 他们分别表示了该用户的ID以及多少个用户被该用户follow。

  再接下来的$2\times k$ 个元素描述了那些用户follow了用户 v1，第一个元素代表了某一个关注用户v1的ID，第二元素代表了这个关注是否为相互的（若为1，则代表了用户v1也关注了该用户；若为0，则代表了用户v1并未关注此用户）

*****



## Dynamic following network

这部分数据包含了某一个用户id1在t时刻关注了id2的数据

涉及的文件为“graph_170w_1month.txt”

文件格式如下：

- 每一行包含三个数据，分别为 id1 id2 t 代表了id1 在t 时刻关注了 id2

*****



