## 二分木 + AVL木の実装

### 構造
-Tree         : 木構造の抽象クラス  
-- BinaryTree : Treeを継承したO(N)の二分木  
-- AVLTree    : Treeを継承したO(logN)のAVL木  

### usage

#### init
```
>>> from Tree import BinaryTree,AVLTree
>>> tree = BinaryTree() #or AVLTree()
```
#### insert and traverse, delete
```
>>> for e in range(10):
>>>     tree = tree.insert(e)
>>> tree.traverse_in_order()
[0,1,2,3,4,5,6,7,8,9]
>>> tree = tree.delete(3)
>>> tree.traverse_in_order()
[0,1,2,4,5,6,7,8,9]
```
#### search
```
>>> tree.search(5)
True
>>> tree.search(10)
False
```
### 参考
http://www.geocities.jp/m_hiroi/light/pyalgo12.html

