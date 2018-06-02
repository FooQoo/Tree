# -*- coding: utf-8 -*-
from abc import ABCMeta,abstractmethod
from graphviz import Digraph

"""課題用木構造モジュール

# 構造
-Tree         : 木構造の抽象クラス
-- BinaryTree : Treeを継承したO(N)の二分木
-- AVLTree    : Treeを継承したO(logN)のAVL木

# usage

## init
>>> from Tree import BinaryTree,AVLTree
>>> tree = BinaryTree() #or AVLTree()

## insert and traverse, delete
>>> for e in range(10):
>>>     tree = tree.insert(e)
>>> tree.traverse_in_order()
[0,1,2,3,4,5,6,7,8,9]
>>> tree = tree.delete(3)
>>> tree.traverse_in_order()
[0,1,2,4,5,6,7,8,9]

## search
>>> tree.search(5)
True
>>> tree.search(10)
False

# 参考
http://www.geocities.jp/m_hiroi/light/pyalgo12.html

"""

class Tree(metaclass=ABCMeta):
    # 子ノードへの左右(L・R)どちらかのpathを示す
    L   = 0
    R   = 1
    
    def __init__(self,v=None,left=None,right=None):
        self.v = v
        self.left  = left
        self.right = right
    
    @abstractmethod
    def insert(self,v):
        pass
    
    @abstractmethod
    def delete(self,v):
        pass
    
    """深さ優先探索
    
    @param  int v    検索する整数
    @return []  path 通過したnodeの値vの配列
    
    """
    def depth_first_search(self,v=None):
        
        if self.v is None:
            return None
        
        stack = []
        stack.append(self)
        path = []
        
        while len(stack) > 0:
            node = stack.pop()
            
            if node.v == v:
                break
            
            # pre-orderと同じ向きになるようRLの順でstackに積む
            if node.right is not None:
                stack.append(node.right)
                
            path.append(node.v)
                
            if node.left is not None:
                stack.append(node.left)
                
        return path
    
    """幅優先探索
    
    @param  int v    検索する整数
    @return []  path 通過したnodeの値vの配列
    
    """
    def breadth_first_search(self,v=None):
        
        if self.v is None:
            return None
        
        queue = []
        queue.append(self)
        path = []
        
        while len(queue) > 0:
            node = queue.pop(0)
            
            if node.v == v:
                break
            
            if node.left is not None:
                queue.append(node.left)
            
            path.append(node.v)
            
            if node.right is not None:
                queue.append(node.right)
                
        return path
    
    """巡回 (pre-order)
    
    @return [] sorted_list 通過したnodeの値vの配列
    
    """
    def traverse_in_order(self):

        sorted_list = []
        node = self
        stack = []
        done = False

        while not done:
            
            # 左へ進み, stackにnodeを積む
            if node is not None:
                stack.append(node)
                node = node.left
                
            else:
                # 左子ノードがNoneかつstackの0でなければ
                if(len(stack) > 0):
                    ## stackからpopして, rightに移動
                    node = stack.pop()
                    
                    ## valueをsorted_listへ追加し, 最初に戻る
                    sorted_list.append(node.v)

                    node = node.right

                else:
                    done = True

        return sorted_list
    
    """検索
    
    @param  int v   検索する整数
    @return int cnt ヒットまでの比較回数(計算量), 見つからない場合は0を出力
    
    """
    def search(self,v):
        
        node = self
        cnt  = 0
        while node is not None:
            
            if node.v is None:
                break

            if node.v == v:
                return cnt

            elif v < node.v:
                cnt += 1
                node = node.left
            else:
                cnt += 1
                node = node.right
                
        return 0
    
    """graphvizへの出力

    @param  BinaryTree node 出力する二分木
    @return Digraph G       jupyterで出力するとinlineで画像が出力される

    """
    def export_graphviz_tree(self):

        if self.v is None:
                return None

        queue = []
        queue.append(self)
        edges = []

        while len(queue) > 0:
            node = queue.pop(0)

            # 再帰と同じ向きである
            if node.left is not None:
                queue.append(node.left)
                edges.append((node.v,node.left.v,'L'))

            if node.right is not None:
                queue.append(node.right)
                edges.append((node.v,node.right.v,'R'))

        # 有向グラフの初期化
        G = Digraph(format='png')
        G.attr('node', shape='circle')

        n_set = set()
        
        for (from_node,to_node,arrow) in edges:
            # ノードの生成
            n_set.add(str(from_node))
            n_set.add(str(to_node))
            
            G.edge(str(from_node), str(to_node),label=arrow)
        
        if len(n_set) == 0:
            return None
        
        for n in list(n_set):
            G.node(n)
            
        return G

class BinaryTree(Tree):
    
    def __init__(self, v=None, left=None, right=None):
        super().__init__(v=v, left=left, right=right)
    
    """挿入
    
    @param  int v      挿入する整数
    @return BinaryTree 追加後の二分木を返す
    
    """
    def insert(self,v):

        # self nodeの処理
        if self.v is None:
            self.v = v
            return self

        node = self

        while node is not None:

            if node.v > v:

                # leftの有無
                if node.left is not None:
                    node = node.left
                else:
                    node.left = BinaryTree(v=v)
                    break

            elif node.v < v:

                # rightの有無
                if node.right is not None:
                    node = node.right
                else:
                    node.right = BinaryTree(v=v)
                    break

            elif node.v == v:
                return self
            
        return self
    
    """削除
    
    @param  int v      削除する整数
    @return BinaryTree 削除後の二分木を返す
    
    """
    def delete(self, v):
        # 空の木を返す
        if self.v is None: 
            return self   
        
        path = []
        # 対象ノードの探索
        node,path = self.__search_delnode(v, path)
        
        # もし削除データがないなら
        if node is None: 
            return self
        
        # 子が二つある場合
        if node.left is not None and node.right is not None:
            
            # 右部分木の最小値を探して置き換える
            path.append((node, self.R))
            min_node = self.__search_min(node.right, path)
            # nodeに格納されているノードに値を代入
            node.v = min_node.v
            # nodeの変数(容器)にmin_nodeを交換するイメージ
            node = min_node
        
        # 挿入したノードの親ノードを取り出す
        # pnode - 挿入されたノードの親ノード
        if len(path) > 0:
            pnode, Dir = path[len(path) - 1]
        else:
            pnode = None
            
        # 右ノードを子ノードの変数にセットする
        if node.left is None:
            cnode = node.right
        # 左ノードを子ノードの変数にセットする
        else:
            cnode = node.left
        
        # 親ノードがない場合
        if pnode is None:
            # 木全てが消去される場合
            if cnode is None:
                return BinaryTree()
            # rootが削除される場合
            else:
                return cnode
        # 親ノードから見て左に進んだ場合
        elif Dir == self.L:
            pnode.left = cnode
        # 親ノードから見て右に進んだ場合
        else:
            pnode.right = cnode
        
        return self
    
    """検索 (削除用)
    
    @param  int v      削除する整数, [] path 削除までに通ったnode(部分木)と分岐した方向(L,R)のタプルのリスト
    @return BinaryTree 削除後の二分木を返す
    
    """
    def __search_delnode(self,v,path=[]):
        
        node = self
        while node is not None:

            if node.v == v:
                return node,path

            elif v < node.v:
                path.append((node,self.L))
                node = node.left
            else:
                path.append((node,self.R))
                node = node.right

        return None,[]

    """最小値検索 (削除用)
    
    @param  BinaryTree node 探索する右部分木, [] path 削除までに通ったnode(部分木)と分岐した方向(L,R)のタプルのリスト
    @return BinaryTree 削除後の二分木を返す
    
    """
    def __search_min(self,node,path):
        
        # 左子ノードがNoneになるまで探索し続ける
        while node.left is not None:
            path.append((node,self.L))
            node = node.left

        return node

class AVLTree(Tree):
    
    def __init__(self,v=None,left=None,right=None,balance=0):
        super().__init__(v=v, left=left, right=right)
        self.balance = balance
    
    """挿入
    
    @param  int v      挿入する整数
    @return BinaryTree 追加後の二分木を返す
    
    """
    def insert(self,v):
        
        path = []

        # self nodeの処理
        if self.v is None:
            self.v = v
            return self

        node = self

        while node is not None:

            if node.v > v:
                path.append((node,self.L))

                # leftの有無
                if node.left is not None:
                    node = node.left
                else:
                    node.left = AVLTree(v=v)
                    break

            elif node.v < v:
                path.append((node,self.R))

                # rightの有無
                if node.right is not None:
                    node = node.right
                else:
                    node.right = AVLTree(v=v)
                    break

            elif node.v == v:
                return self
        
        return self.__balance_insert(path)
    
    """木の修正 (挿入)
    
    @param  BinaryTree node 探索する右部分木, [] path 削除までに通ったnode(部分木)と分岐した方向(L,R)のタプルのリスト
    @return BinaryTree 削除後の二分木を返す
    
    - Algorithm memo
    1. 挿入位置から根まで移動
    2. pathに応じて親ノードのbalanceを+1 or -1
    3. 親ノードと子ノードのbalanceに応じて, 回転方向を決定
    4. 回転後はbalanceを調整する
    5. pathが残っている場合はnew_nodeを上位ノードに付け替え
    """
    def __balance_insert(self,path):
        
        node = self
        new_node = None

        # 挿入したノードから根まで登る
        # pathがなくなるまで繰り返し
        while len(path) > 0:

            # 親ノード(pnode)と親ノードからのpath
            pnode,Dir = path.pop()

            # pnodeから左方向のpathなら
            if Dir == self.L:
                # pnodeの平衡度が+1される
                pnode.balance += 1
            # pnodeから右方向のpathなら
            else:
                # pnodeの平衡度が-1される
                pnode.balance -= 1

            # b = 親ノードの平衡度
            b = pnode.balance

            # 親ノードの平衡度が0なら修正不要であり, 根を返す
            if b == 0:
                return self

            # 親ノードの平衡度が2以上
            if b > 1:
                # かつ親ノードからの左子ノードが-1以下ならば
                if pnode.left.balance < 0:
                    # LR2重回転

                    # 左部分木を左回転(pnode.leftの部分木のみ回転する)
                    pnode.left = self.__rotate_left(pnode.left)
                    # 親から見た部分木を右回転(新しい根を獲得)
                    new_node   = self.__rotate_right(pnode)
                    # 平衡度の更新(二重回転した場合)
                    self.__update_balance(new_node)
                else:
                    # LL1重回転

                    # 親ノードを右回転(新しい根を獲得)
                    new_node   = self.__rotate_right(pnode)
                    # 回転後の平衡度は0
                    new_node.balance = 0
                    pnode.balance = 0
                break

            # 親ノードの平衡度が-2以下
            elif b < -1:
                # かつ親ノードからの右子ノードが1以上ならば
                if pnode.right.balance > 0:
                    # RL 2重回転

                    # 右部分木を右回転
                    pnode.right = self.__rotate_right(pnode.right)
                    # 親から見た部分木を左回転
                    new_node    = self.__rotate_left(pnode)
                    # 平衡度の更新
                    self.__update_balance(new_node)
                else:
                    # RR 1重回転

                    # 親から見た部分木を左回転
                    new_node = self.__rotate_left(pnode)
                    # 回転後の平衡度は0
                    new_node.balance = 0
                    pnode.balance = 0
                break

        # pathがまだ残っている場合，修正を行なった部分木の親ノードの子を付け替える必要がある
        if len(path) > 0:
            # pnodeの親節を求める
            gnode, gdir = path.pop()

            # pnodeが左部分木なら
            if gdir == self.L:
                # pnodeの親ノードの左子を更新
                gnode.left = new_node
            else:
                # pnodeの親ノードの右子を更新
                gnode.right = new_node

        # pathにデータがないかつ部分木がNoneでなければnew_nodeを親木として返す
        elif new_node is not None:
            return new_node
        # new_nodeがNoneなら木の修正は行われていない
        
        # 全体の木を返す
        return self
    
    """削除
    
    @param  int v      削除する整数
    @return BinaryTree 削除後の二分木を返す
    
    """
    def delete(self, v):
        # 空の木を返す
        if self.v is None: 
            return self  
        
        # 経路
        path = []
        # 対象ノードの探索
        node,path = self.__search_delnode(v, path)
        
        # もし削除データがないなら
        if node is None: 
            return self
        
        # 子が二つある場合
        if node.left is not None and node.right is not None:
            
            # 右部分木の最小値を探して置き換える
            path.append((node, self.R))
            min_node = self.__search_min(node.right, path)
            # nodeに格納されているノードに値を代入
            node.v = min_node.v
            # nodeの変数(容器)にmin_nodeを交換するイメージ
            node = min_node
        
        # 挿入したノードの親ノードを取り出す
        # pnode - 挿入されたノードの親ノード
        if len(path) > 0:
            pnode, Dir = path[len(path) - 1]
        else:
            pnode = None
            
        # 右ノードを子ノードの変数にセットする
        if node.left is None:
            cnode = node.right
        # 左ノードを子ノードの変数にセットする
        else:
            cnode = node.left
        
        # 親ノードがない場合
        if pnode is None:
            # 木全てが消去される場合
            if cnode is None:
                return AVLTree()
            # rootが削除される場合
            else:
                return cnode
        # 親ノードから見て左に進んだ場合
        elif Dir == self.L:
            pnode.left = cnode
        # 親ノードから見て右に進んだ場合
        else:
            pnode.right = cnode
        
        return self.__balance_delete(path)
    
    """木の修正 (削除)
    
    @param  BinaryTree node 探索する右部分木, [] path 削除までに通ったnode(部分木)と分岐した方向(L,R)のタプルのリスト
    @return BinaryTree 削除後の二分木を返す
    
    """
    def __balance_delete(self, path):
        # pathが1つでもあれば継続
        while len(path) > 0:
            new_node = None
            
            # 親ノードを取り出す
            pnode, Dir = path.pop()
            
            # 親から見て左の場合 +1
            if Dir == self.L:
                pnode.balance -= 1
            # 親から見て右の場合 -1
            else:
                pnode.balance += 1
            
            # 親ノードの平衡度
            b = pnode.balance
            if b > 1:
                if pnode.left.balance < 0:
                    # 親ノードの平衡度が2以上かつ親ノードの左子ノードが0未満なら
                    # LR二重回転 
                    # 0未満のノードで左回転
                    pnode.left = self.__rotate_left(pnode.left)
                    # 2以上のノードで右回転
                    new_node   = self.__rotate_right(pnode)
                    # 平衡度の調整
                    self.__update_balance(new_node)
                else:
                    # LL一重回転 
                    # 根ノードで右回転
                    new_node = self.__rotate_right(pnode)
                    
                    # 部分木の根 : 2, 左子(new_node.balance) : 0
                    # 1, -1
                    if new_node.balance == 0:
                        new_node.balance = -1
                        pnode.balance = 1
                    # 部分木の根 : 2, 左子(new_node.balance) : 1
                    # 0, 0
                    else:
                        new_node.balance = 0
                        pnode.balance = 0
            elif b < -1:
                if pnode.right.balance > 0:
                    # 親ノードの平衡度が-2以下かつ親ノードの右子ノードが0より大きいなら
                    # RL二重回転 
                    # 0未満のノードで左回転
                    pnode.right = self.__rotate_right(pnode.right)
                    new_node = self.__rotate_left(pnode)
                    self.__update_balance(new_node)
                else:
                    # RR一重回転 
                    # 根ノードで左回転
                    
                    new_node = self.__rotate_left(pnode)
                    # 部分木の根 : -2, 左子(new_node.balance) : 0
                    # 1, -1
                    if new_node.balance == 0:
                        new_node.balance = 1
                        pnode.balance = -1
                    # 部分木の根 : -2, 右子(new_node.balance) : 1
                    # 0, 0
                    else:
                        new_node.balance = 0
                        pnode.balance = 0
                        
            # b == 1 or b == -1 は修正終了
            # bが0になると高さが変わる
            elif b != 0:
                break   
                
            # 子の付け替え
            if new_node is not None:
                # すでにpathがないなら根として返す
                if len(path) == 0: 
                    return new_node
                
                # 部分木を子に持つノードを取り出す
                gnode, gdir = path[len(path) - 1]
                
                # 左部分木なら左子ノードに接続
                if gdir == self.L:
                    gnode.left = new_node
                # 右部分木なら右子ノードに接続
                else:
                    gnode.right = new_node
                
                if new_node.balance != 0: 
                    break      # 修正終了
        return self
    
    """検索 (削除用)
    
    @param  int v      削除する整数, [] path 削除までに通ったnode(部分木)と分岐した方向(L,R)のタプルのリスト
    @return BinaryTree 削除後の二分木を返す
    
    """
    def __search_delnode(self,v,path=[]):
        
        node = self
        while node is not None:

            if node.v == v:
                return node,path

            elif v < node.v:
                path.append((node,self.L))
                node = node.left
            else:
                path.append((node,self.R))
                node = node.right

        return None,[]

    """最小値検索 (削除用)
    
    @param  BinaryTree node 探索する右部分木, [] path 削除までに通ったnode(部分木)と分岐した方向(L,R)のタプルのリスト
    @return BinaryTree 削除後の二分木を返す
    
    """
    def __search_min(self,node,path):
        
        # 左子ノードがNoneになるまで探索し続ける
        while node.left is not None:
            path.append((node,self.L))
            node = node.left

        return node
    
    """右回転
    @param  BinaryTree node 探索する部分木
    @return BinaryTree 回転後の二分木を返す
    
    """
    def __rotate_right(self,node):
        if node.left is None:
            return node
        else:
            lnode = node.left
            # 左子ノードの右子ノードを左子ノードの移動
            node.left = lnode.right
            # 元ノードを左子ノードの右子ノードに移動
            lnode.right = node
            # 回転後は左子ノードが部分木の根になる
            return lnode

    """左回転
    @param  BinaryTree node 探索する部分木
    @return BinaryTree 回転後の二分木を返す
    
    """
    def __rotate_left(self,node):
        if node.right is None:
            return node
        else:
            rnode = node.right
            # 右子ノードの左子ノードを右子ノードに移動
            node.right = rnode.left
            # 元ノードを左子ノードを右子ノードに移動
            rnode.left = node
            # 回転後は右子ノードが部分木の根になる
            return rnode

    """二重回転(LR・RL)後の平衡度修正
    
    @param  BinaryTree node 探索する部分木
    
    """
    def __update_balance(self,node):
        # LR二重回転の時では元親ノードが1であるから
        if node.balance == 1:
            # 元親ノード
            node.right.balance = -1
            # 元左子ノード
            node.left.balance = 0

        # RL二重回転の時では元親ノードが-1であるから
        elif node.balance == -1:
            # 元親ノード
            node.right.balance = 0
            # 元右子ノード
            node.left.balance = 1
        else:
            node.right.balance = 0
            node.left.balance = 0
        
        # 部分木の根の平衡度は0
        node.balance = 0