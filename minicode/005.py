# coding:utf-8
import numpy as np


def cross_entropy(arr):
    arr = arr/np.sum(arr)
    return -np.sum(arr*np.log2(arr))

def square_loss(arr):
    return np.sum(arr*arr) - arr.shape[0] * (np.mean(arr))**2

# 算法5.1
# 定义5.2
def calculate_information_gain(dataset, attribute):
    H_D = cross_entropy(np.unique(dataset[:,-1], return_counts=True)[1])
    uni, fre = np.unique(attribute, return_counts=True)
    fre = fre / np.sum(fre)
    d = [dataset[(attribute==i).squeeze()] for i in uni]
    for i in range(len(uni)):
        fre[i] *= cross_entropy(np.unique(d[i][:,-1], return_counts=True)[1])
    H_DA = np.sum(fre)
    return H_D, H_DA

# 定义5.3
def calculate_information_gain_ratio(dataset, attribute):
    g = calculate_information_gain(dataset, attribute)
    if g[0] == 0:
        return 0
    return 1-g[1]/g[0]


# 算法5.2, 5.4
class ID3:
    def __init__(self, dataset, e, parent=None, feature=None, build=True, alpha=0):
        self.dataset = dataset
        self.feature = feature
        self.prediction = None
        self.accuracy = 0
        self.e = e
        self.g = 0
        self.arg_g = 0
        self.alpha = alpha
        self.cost = dataset.shape[0] * cross_entropy(
            np.unique(dataset[:,-1], return_counts=True)[1]) + self.alpha
        self.children_cost = 0
        self.parent = parent
        self.children = []
        if self.parent != None:
            self.parent.children_cost += self.cost
        if build:
            self.build_tree()
    
    def build_tree(self):
        self.find_best_feature()
        if self.g < self.e:
            return
        self.split_dataset_by_feature()
        self.pruning()

    def find_best_feature(self):
        gain = [calculate_information_gain(self.dataset, self.dataset[:,i]) 
            for i in range(self.dataset.shape[-1] - 1)]
        for i in range(len(gain)):
            gain[i] = gain[i][0]-gain[i][1]
        self.g = np.max(gain)
        self.arg_g = np.argmax(gain)

    def split_dataset_by_feature(self):
        uni = np.unique(self.dataset[:,self.arg_g])
        for i in uni:
            dataset = self.dataset[(self.dataset[:,self.arg_g]==i).squeeze()]
            self.children.append(
                ID3(np.delete(dataset, self.arg_g, 1), 
                    self.e, parent=self, feature=i, alpha=self.alpha)
            )

    def walk(self):
        print(self.dataset)
        print(f'gain:{self.g:.3f},column:{self.arg_g}')
        if len(self.children) != 0:
            [x.walk() for x in self.children]

    def generate_prediction(self):
        uni, fre = np.unique(self.dataset[:,-1], return_counts=True)
        self.prediction = uni[np.argmax(fre)]
        for x in self.children:
            x.generate_prediction()

    def calculate_accuracy(self):
        if len(self.children) == 0:
            if self.parent == None:
                self.accuracy = np.sum(self.dataset[:,-1]==self.prediction) / self.dataset.shape[0]
                return
            return np.sum(self.dataset[:,-1]==self.prediction), self.dataset.shape[0]
        s_c, s_t = 0, 0
        for x in self.children:
            correct, total = x.calculate_accuracy()
            s_c += correct
            s_t += total
        self.accuracy = s_c / s_t
        return s_c, s_t
    
    def pruning(self):
        if self.children_cost >= self.cost:
            self.children = []
        elif self.parent != None:
            self.parent.children_cost -= self.cost - self.children_cost



# 算法5.3
class C4_5(ID3):
    def __init__(self, dataset, e, feature=None, parent=None, alpha=0):
        ID3.__init__(self, dataset, e, feature=feature, parent=parent, build=False, alpha=alpha)
        self.build_tree()
    
    def find_best_feature(self):
        gain = [calculate_information_gain_ratio(self.dataset, self.dataset[:,i]) 
            for i in range(self.dataset.shape[-1] - 1)]
        self.g = np.max(gain)
        self.arg_g = np.argmax(gain)
    
    def split_dataset_by_feature(self):
        uni = np.unique(self.dataset[:,self.arg_g])
        for i in uni:
            dataset = self.dataset[(self.dataset[:,self.arg_g]==i).squeeze()]
            self.children.append(
                C4_5(np.delete(dataset, self.arg_g, 1), 
                    self.e, feature=i, parent=self, alpha=self.alpha)
            )


def main():
    # 表5.1
    dataset = np.array([
        [0,0,0,0,0],
        [0,0,0,1,0],
        [0,1,0,1,1],
        [0,1,1,0,1],
        [0,0,0,0,0],
        [1,0,0,0,0],
        [1,0,0,1,0],
        [1,1,1,1,1],
        [1,0,1,2,1],
        [1,0,1,2,1],
        [2,0,1,2,1],
        [2,0,1,1,1],
        [2,1,0,1,1],
        [2,1,0,2,1],
        [2,0,0,0,0],
    ])
    attr = dataset[:,3]
    # print(calculate_information_gain(dataset, attr))
    # print(calculate_information_gain_ratio(dataset, attr))
    # root = ID3(dataset, 0.4, alpha=1)
    # root.walk()
    root = C4_5(dataset, 0.1, alpha=1)
    # root.walk()
    root.generate_prediction()
    root.calculate_accuracy()
    # print(root.accuracy)
    
    print(square_loss(np.array([1,2,3])))

if __name__ == "__main__":
    main()
