import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

from sklearn.datasets import load_digits
#from sklearn.decomposition import PCA


def run():

 digits=load_digits()
 print(digits.data.shape)
 numpca=digits.data.shape[1]



#plot stuff

 # set up the figure
 fig = plt.figure(figsize=(6, 6))  # figure size in inches
 fig.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0.05, wspace=0.05)

# plot the digits: each image is 8x8 pixels
 for i in range(64):
    ax = fig.add_subplot(8, 8, i + 1, xticks=[], yticks=[])
    ax.imshow(digits.images[i], cmap=plt.cm.binary, interpolation='nearest')
    
    # label the image with the target value
    ax.text(0, 7, str(digits.target[i]))

 plt.show()
 
#Step 1
 digits_mean=digits.data-np.mean(digits.data,axis=0)

#Step 2
 cov=np.matmul(digits_mean.T,digits_mean)

#Step 3
 eig_val,eig_vec=np.linalg.eigh(cov)

#Step 4
 indices=np.argsort(eig_val)[::-1]
 eig_val=eig_val[indices]
 eig_vec=eig_vec[:,indices]

#Step 5
 n_comp=numpca
 eig_vec=eig_vec[:,:numpca]
 eig_valtot=eig_val
 eig_val=eig_val[:numpca]

 pca_components=((digits_mean).dot(eig_vec))

 plt.scatter(pca_components[:, 0], pca_components[:, 1],
             c=digits.target, edgecolor='none', alpha=0.5,
             cmap=plt.cm.get_cmap('nipy_spectral', 10))
 plt.xlabel('component 1')
 plt.ylabel('component 2')
 plt.colorbar()
 
 plt.show()

### Plotting the contribution of each PC to the total variance
 totvar=np.sum(eig_valtot)

 explained_var_ratio=eig_valtot/totvar

#Computing the Cumulative Variance of each eigenvector/PC

 plt.bar(range(0,len(explained_var_ratio)),explained_var_ratio,alpha=0.5,align='center',label='Individual Explained Variance',color='orange' ) 
 plt.plot(np.cumsum(explained_var_ratio),marker='o',label='Cumulative Explained Variance')
 plt.xlabel('number of components')
 plt.ylabel('cumulative explained variance')
 plt.legend(loc='best')
 plt.tight_layout()

 plt.show()

 #pca = PCA(n_components=18)
 #Xproj = pca.fit_transform(digits.data)
 sns.set_style('white')

 #print(Xproj[10])
 fig = plot_pca_components(digits.data[10], pca_components[10],
                           np.mean(digits.data,axis=0), eig_vec.T)
 
 
 plt.show()
 #exit()

 #print(Xproj[15])
 fig = plot_pca_components(digits.data[15], pca_components[15],
                           np.mean(digits.data,axis=0), eig_vec.T)

 print('pcacomponents ',pca_components[15]) 
 
 plt.show()


def plot_pca_components(x, coefficients=None, mean=0, components=None,
                        imshape=(8, 8), n_components=8, fontsize=10,
                        show_mean=True):
    if coefficients is None:
        coefficients = x
        
    if components is None:
        components = np.eye(len(coefficients), len(x))
        
    mean = np.zeros_like(x) + mean
        

    fig = plt.figure(figsize=(1.2 * (5 + n_components), 1.2 * 2))
    g = plt.GridSpec(2, 4 + bool(show_mean) + n_components, hspace=0.3)

    def show(i, j, x, title=None):
        ax = fig.add_subplot(g[i, j], xticks=[], yticks=[])
        ax.imshow(x.reshape(imshape), interpolation='nearest')
        if title:
            ax.set_title(title, fontsize=fontsize)

    show(slice(2), slice(2), x, "True")
    
    approx = mean.copy()
    
    counter = 2
    if show_mean:
        show(0, 2, np.zeros_like(x) + mean, r'$\mu$')
        show(1, 2, approx, r'$1 \cdot \mu$')
        counter += 1

#    print('ncomponents \n',n_components)
#    print('coefficients \n',coefficients)
#    print('components \n',components)
#    print(len(coefficients),coefficients.shape)
#    print(len(components),components.shape)

    for i in range(n_components):
        approx = approx + coefficients[i] * components[i]
        show(0, i + counter, components[i], r'$c_{0}$'.format(i + 1))
        show(1, i + counter, approx,
             r"${0:.2f} \cdot c_{1}$".format(coefficients[i], i + 1))
        if show_mean or i > 0:
            plt.gca().text(0, 1.05, '$+$', ha='right', va='bottom',
                           transform=plt.gca().transAxes, fontsize=fontsize)

    show(slice(2), slice(-2, None), approx, "Approx")
    return fig

