# coding:utf-8
import numpy as np

# balanced k-d Tree
# 实现了k近邻法的特例最近邻，对应算法3.2、3.3

class kdnode():
    def __init__(self, points, dim, parent=None):
        self.dim = dim
        self.parent = parent
        idx = np.argsort(points[:,self.dim])
        split_point = idx.shape[0]//2
        self.point = points[idx[split_point]]
        self.lchild = kdnode(points=points[idx[:split_point]], 
                    dim=(self.dim+1)%points.shape[-1], 
                    parent=self) if split_point != 0 else None
        self.rchild = kdnode(points=points[idx[split_point+1:]], 
                    dim=(self.dim+1)%points.shape[-1], 
                    parent=self) if split_point != idx.shape[0] - 1 else None
    
    def walk(self):
        print(self.point)
        if self.lchild != None:
            self.lchild.walk()
        if self.rchild != None:
            self.rchild.walk()
    
    def search(self, pt):
        if pt[self.dim] < self.point[self.dim] and self.lchild != None:
            return self.lchild.search(pt)
        elif self.rchild != None:
            return self.rchild.search(pt)
        else:
            return self
    
    def is_intersected(self, pt, min_dist):
        return min_dist > np.abs(self.point[self.dim] - pt[self.dim])

    def backtoroot(self, pt, min_dist, nearest_node, root):
        if np.linalg.norm(self.point - pt) < min_dist:
            nearest_node = self
            min_dist = np.linalg.norm(nearest_node.point - pt)
        if self == root:
            return nearest_node
        if self == self.parent.lchild:
            peer = self.parent.rchild
        else:
            peer = self.parent.lchild
        if peer is not None and peer.is_intersected(pt, min_dist):
            tmp_node = peer.search(pt)
            tmp_dist = np.linalg.norm(tmp_node.point - pt)
            tmp_node = tmp_node.backtoroot(pt, tmp_dist, tmp_node, peer)
            if np.linalg.norm(tmp_node.point - pt) < min_dist:
                nearest_node = tmp_node
                min_dist = np.linalg.norm(nearest_node.point - pt)
        return self.parent.backtoroot(pt, min_dist, nearest_node, root)

        

class kdTree():
    def __init__(self, points):
        self.k = points.shape[-1]
        self.points = points
        self.root = kdnode(points,0)
        self.min_dist = None
        self.nearest_node = None
    
    def walk(self):
        self.root.walk()

    def nearest_search(self, pt):
        self.nearest_node = self.root.search(pt)
        self.min_dist = np.linalg.norm(self.nearest_node.point - pt)
        self.nearest_node = self.nearest_node.backtoroot(pt, self.min_dist, self.nearest_node, self.root)
        self.min_dist = np.linalg.norm(self.nearest_node.point - pt)
        print(self.nearest_node.point, self.min_dist)


if __name__ == "__main__":
    pt = np.array([[2,3],[5,4],[9,6],[4,7],[8,1],[7,2]])
    # print(pt)
    kdt = kdTree(pt)
    kdt.nearest_search([5,3])