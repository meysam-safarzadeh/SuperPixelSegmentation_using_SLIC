# Super Pixel Segmentation Using SLIC

## Goals and perspectives

In this project, the goal is to segment rover, background, and shadow (if any). In this part of the report we are going to use simple linear iterative clustering (SLIC), and adaptive SLIC for initial segmentation. Next, we want to implement a region adjacency graph (RAG) on the regions obtained from the segmentation algorithm. Finally, to handle the over-segmentation, Hierarchical merging, and Normalized cuts will be used. The illustration of the whole procedure is shown in Figure 1. In the next sections, implementation, comparison, and interpretation of the models will be discussed in detail. 

![image](https://user-images.githubusercontent.com/51737180/210186847-7df27303-2378-4e57-897a-77c8ae6aeaf3.png)


## Data
Our data consists of four images. All of them are in RGB color space. Picture 0 has three objects including rover, background, and shadow; and the rest of them are without shadow. Figures 1 to 4 are the original images before any processing.

<img src="https://user-images.githubusercontent.com/51737180/210186806-ff82405a-0117-4252-8086-ca8d5cf21eb7.png" width="400"> <img src="https://user-images.githubusercontent.com/51737180/210186813-436fba72-2889-4ae2-85dc-aa4bf8b30775.png" width="400">

Figure 1 and 2

<img src="https://user-images.githubusercontent.com/51737180/210186819-5984571b-091c-441b-97a3-bfb8f1445388.png" width="400"> <img src="https://user-images.githubusercontent.com/51737180/210186823-8ca1f3af-c552-4770-a685-2a534818d75f.png" width="400">

Figure 3 and 4

## SLIC
Simple linear iterative clustering (SLIC) utilized a k-means algorithm to generate superpixels that are supposed to adherence object boundaries in the image. It has two parameters to adjust which are the number of superpixels to generate and compactness. Moreover, the input image should be in CIELAB color space which we utilized skimage.segmentation.slic function that automatically changes the color space of the input image. To begin with, we set 200 for the k (number of superpixels), and 10 for compactness which is the default of their method [^1]. Usually, compact superpixels are more desirable but increasing the compactness may result in reduced boundary adherence [1]. Figure 5 shows the output label of the SLIC algorithm, and Figure 6 shows superpixels with boundaries in the original image.
At this stage, we should tune these two parameters in a way that superpixels boundaries do not exceed the boundaries of the objects which in Figure 6 is not satisfied at certain areas circled by a red line. Therefore, in the next attempt, we can make it more compact in order to approach the desired over-segmentation. In Figure 7, it is shown that by increasing the compactness the result is more desirable yet some superpixels do not adherent the boundaries which are shown in a red circle. This problem should be because of the number of segments. Since the algorithm is supposed to generate superpixels roughly equal in size. Therefore, to continue tuning, we can increase the number of segments to generate more desirable superpixels. Figure 8 shows the results of increasing the number of segments to 600. The mentioned spot is segmented a little better by this tuning yet it can be better. 

![image](https://user-images.githubusercontent.com/51737180/210186910-6da1f5ce-57fc-41a3-9751-df4953a45b42.png)

Figure 6

![image](https://user-images.githubusercontent.com/51737180/210186920-4f23e6e3-1b8b-4884-9b84-3b79d6c0b4ef.png)

Figure 7

![image](https://user-images.githubusercontent.com/51737180/210186935-8c619851-721e-4a14-8c03-4eb36f8346ca.png)

Figure 8

[^1]: R. Achanta, A. Shaji, K. Smith, A. Lucchi, P. Fua, and S. Süsstrunk, “SLIC Superpixels Compared to State-of-the-Art Superpixel Methods,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 34, no. 11, pp. 2274–2282, Nov. 2012, doi: 10.1109/TPAMI.2012.120.

Furthermore, in the method [^1] they stated that the number of iterations is 10 which is suitable for most images, but we intend to investigate this further. To do so, we increased the number of iterations to 50. The result is shown in Figure 9. Also, Figure 10 shows the above-mentioned spot in Figure 9 which is segmented very well. Consequently, we select these parameters as a well-tuned one, although in some other cases are still not perfect. Figure 11 shows the over-segmentation result obtained by the SLIC algorithm after parameter tuning. SLIC segmentation on the original image and without that for picture 2 are shown in Figures 12 and 13 respectively. Moreover, these results for pictures 1 and 0 are shown in Figures 14, 15, 16, and 17 respectively. By looking at the results of SLIC in other pictures, we can conclude that the parameters are promising, and can help the merging algorithms (Hierarchical and Ncuts) very well. In the next part, we are going to try adaptive SLIC and compare it with SLIC.

![image](https://user-images.githubusercontent.com/51737180/210186946-119c8a69-68e8-4201-891b-c02cd389e082.png)
![image](https://user-images.githubusercontent.com/51737180/210186949-fdef7237-b764-40e1-ab61-439617941f19.png)

Figure 9 and 10

![image](https://user-images.githubusercontent.com/51737180/210186954-94c3a3c8-8999-4987-8be2-1dfaab090814.png)
![image](https://user-images.githubusercontent.com/51737180/210186956-8d261106-68a2-4001-894d-405b5e122f06.png)

Figure 11 and 12

![image](https://user-images.githubusercontent.com/51737180/210186964-061fd424-3167-4fdf-9ce9-da23528c944e.png)
![image](https://user-images.githubusercontent.com/51737180/210186968-209720c5-6a83-478b-b570-9f9a56ae2f1c.png)

Figure 13 and 14

![image](https://user-images.githubusercontent.com/51737180/210186971-06870bcd-ea09-48ce-9811-fda0e8ea23ed.png)
![image](https://user-images.githubusercontent.com/51737180/210186973-a2ebac79-416e-4bde-bc1c-9ea990330380.png)

Figure 15 and 16

![image](https://user-images.githubusercontent.com/51737180/210186977-2ffa46fe-accb-4fb5-8208-f14f406fa5ad.png)

Figure 17

## Adaptive SLIC
Adaptive SLIC is similar to the previous version of it except it automatically adapts the compactness based on the region. Therefore, there is no need to tune the compactness and all we have to do is define the number of segments. In order to do a fair comparison between the SLIC methods, we assign 600 for the number of segments (superpixels). Figure 18 shows the segmentation boundaries on the original image and also Figure 19 shows the segmentation labels with the mean intensity of each superpixel. It can be seen that in challenging spots, the accuracy of segmentation is not very well and some superpixels do not adhere to the boundaries of the rover. Figure 20 shows the mentioned spot obtained from SLIC and an adaptive version of it.

![image](https://user-images.githubusercontent.com/51737180/210186988-e248d25b-8dc8-49b5-97f7-016377b523dc.png)
![image](https://user-images.githubusercontent.com/51737180/210186993-e1aea947-d618-430f-ad6d-3b5ea9975663.png)

Figure 18 and 19

![image](https://user-images.githubusercontent.com/51737180/210187000-01564052-472f-4049-aea4-e247dad4f97a.png)
![image](https://user-images.githubusercontent.com/51737180/210187002-f235bc0e-f7f8-4f25-87d6-b89f62f6c8bb.png)

Figure 20 The left picture is obtained from the Adaptive SLIC and the right obtained from SLIC after parameter tuning

As can be seen in Figure 20, some superpixels (shown by the red line) exceed the rover’s boundaries. To conclude, an adaptive version of SLIC cannot overcome the refined version of SLIC. In the next Figures (21 to 26) the segmentation result and labels of pictures 2, 1, and 0 are shown respectively.

![image](https://user-images.githubusercontent.com/51737180/210187019-ba426a82-7f77-4184-905e-972cee301936.png)
![image](https://user-images.githubusercontent.com/51737180/210187022-3b600e32-b431-4a55-9c99-4b49089b02a1.png)

Figure 21 and 22

![image](https://user-images.githubusercontent.com/51737180/210187026-16999a83-f111-4548-8db0-008bc71b1be3.png)
![image](https://user-images.githubusercontent.com/51737180/210187028-b8238c40-ebf0-4168-b5e2-9215e87869c3.png)

Figure 23 and 24

![image](https://user-images.githubusercontent.com/51737180/210187032-0526044e-ffa0-4161-a6f0-1c15c20bdf39.png)
![image](https://user-images.githubusercontent.com/51737180/210187035-ec2e9867-fe91-4dc3-8d31-5a3422e704d9.png)

Figure 25 and 26

## RAG
Region Adjacency Graph is a graph that connects the superpixels and assigns a weight for each connection. This weight represents the Euclidean distance between the average of two superpixels. The more the weight, the more different the mean of those adjacent regions. Figure 27 shows the initial RAG of picture 3 obtained from the SLIC algorithm. Higher values of difference in the mean color of regions are shown with the lighter color. Therefore, the boundaries weights are more than 150 roughly, and regions similar together in terms of the mean of superpixels, have weights less than 25 roughly. In the next Figures (28 to 33), the initial RAG of pictures 2, 1, and 0 are shown respectively.

![image](https://user-images.githubusercontent.com/51737180/210187098-fe2003e6-3c57-4eb2-94d6-43ee723915b2.png)
![image](https://user-images.githubusercontent.com/51737180/210187100-820d4975-c42e-4f8e-b6fd-0156e6672af0.png)

Figure 27 and 28

![image](https://user-images.githubusercontent.com/51737180/210187103-3ae6e82c-3ac0-4eea-a1a6-5bfff07c3f32.png)
![image](https://user-images.githubusercontent.com/51737180/210187107-8ff7b4ac-22fc-4cc8-89d7-287ea76f51ef.png)

Figure 29 and 30

## Hierarchical merging
This method merges the regions with a weight less than a threshold. Therefore, based on the color bar of the previous figures we can choose a proper value for the threshold. In this section, we start investigating from pictures 0 to 3. To begin with, based on the color bar we assign the threshold to 40. The new RAG is shown in Figure 31 with new weights. Also, the segmentation result is shown in Figure 32. As it can be seen, the overall performance is very well, but in some regions which are close in color (weight is low), the segments do not adhere to the boundaries. For instance, the edge of the rover’s scope is not well segmented which is circled by the red line in Figure 32. Perhaps, by reducing the threshold we can overcome this issue a little.

![image](https://user-images.githubusercontent.com/51737180/210187116-f360475d-ae95-44b9-8474-da8167a56e70.png)
![image](https://user-images.githubusercontent.com/51737180/210187129-e1f7bd42-9933-43c0-9fc7-05c0bba365b5.png)

Figure 31 and 32

Let assign 25 for the threshold. Figure 33 shows the result for picture 0. The edge of the scope is better segmented but on the other hand, we faced over-segmentation for the background which is not desirable. Furthermore, for other pictures, based on their color bar we choose a proper threshold in a way that adheres to the boundaries as much as possible. After trying several values for the threshold for picture 1, the best result is shown in Figure 34. It adheres to the boundaries of the rover, although the background is not merged to a unit segment. Nevertheless, as long as it does not exceed the boundaries of the rover, it is acceptable and we can apply further algorithms like morphological operations to merge the background into a unit region. For the next picture, we initially assign 170 based on the color bar and then gradually change it to a better value. After some iterations, we assigned 110 for picture 2. Figure 35 shows the segmentation result of this picture. For the last picture, by trying a couple of values the best result is obtained with a threshold equal to 110. Nonetheless, in some areas, the segments exceed the boundaries of the object which are constant even for thresholds as low as 45. This is because of the similarity between the mean values of the mark on the rover and the background. Other remaining small superpixels again can be merged by morphological operations which we did in the previous project of the course.

![image](https://user-images.githubusercontent.com/51737180/210187189-d5fa524c-0662-4a82-8f31-92bdba2f9bbe.png)
![image](https://user-images.githubusercontent.com/51737180/210187192-e513935b-45bc-4236-a0fe-02eef2ac236d.png)

Figure 33 and 34

![image](https://user-images.githubusercontent.com/51737180/210187195-66151f2b-e9cd-45e5-b548-61d16b0aacf8.png)
![image](https://user-images.githubusercontent.com/51737180/210187205-c6f192ce-7509-4c23-8c39-0ef74223e78d.png)

Figure 35 and 36

Consequently, in order to prevent repetitive over-segmentation, we let the threshold be high. In this way, we can deal with the small remaining regions easier.
Moreover, we tried the SLIC over-segmentation with a much less number of segments which resulted in better outcomes. Figure 37 is the final result of picture 0 after hierarchical merging which is exactly three segments as we expected although the edge of the scope is not well segmented. This is the weakness of the method and to the best of our efforts, it is the best possible result. Furthermore, the final segmentation of pictures 1, 2, and 3 are shown in Figures 38 to 42.

![image](https://user-images.githubusercontent.com/51737180/210187218-eb62ba5b-b39d-4077-87f2-28805603ba89.png)
![image](https://user-images.githubusercontent.com/51737180/210187221-3efa0cb0-06fc-4b70-98f4-1e98dad9b922.png)

Figure 37 and 38

![image](https://user-images.githubusercontent.com/51737180/210187228-24ab7fe3-f261-428b-8fdf-5db9b8925eb9.png)
![image](https://user-images.githubusercontent.com/51737180/210187229-7aa50a5b-6eb5-4a13-b7f1-d306c52b2fbb.png)

Figure 39 and 40

![image](https://user-images.githubusercontent.com/51737180/210187234-2c71a326-b0b1-4489-b2de-3ee7e6e83f6b.png)
![image](https://user-images.githubusercontent.com/51737180/210187237-b0d3f8a5-4df1-4270-9d60-faa2b0d47a4c.png)

Figure 41 and 42

## NCuts
The normalized cuts algorithm is based on a generalized eigenvalue problem that calculates the similarity and dissimilarity between the groups of the graphs. This method has two parameters to tune that is threshold and number of cuts. The threshold defines the margin to control the dividing of the subgraphs. Moreover, the number of cuts is just to initialize the algorithm, and then the algorithm itself can investigate further to find the optimal value for it. By investigating the values for the threshold finally, we assigned 0.005 for it and 30 for the initial number of cuts. Figure 43 shows the result of this configuration in picture 0. Again, the segmentation is suffering from crossing boundaries in superpixels similar together in terms of color (circled by the red line). This is the weakness of both hierarchical and NCuts methods. Although the quality of segmentation is very well in other areas, after trying several numbers of thresholds for the algorithm, it is not able to merge regions of the rover, so the rover is considered as two superpixels which are not proper. This has happened to picture 3 which the final segmentation result has 4 segments although it is expected to be 2. The final segmentation result of picture 3 is shown in Figure 47. On the other hand, pictures 1 and 2 can merge properly with the low crossing of boundaries. Figures 44 and 45 show the result of segmentation of picture 1 after NCuts merging which is crossing the boundaries of the rover (circled by the red line).

![image](https://user-images.githubusercontent.com/51737180/210187329-521fe636-7593-4d77-8489-333325a4cc1f.png)
![image](https://user-images.githubusercontent.com/51737180/210187316-279bce01-4b79-4d2c-9ac6-b7973f9eb55f.png)

Figure 43 and 44

![image](https://user-images.githubusercontent.com/51737180/210187300-94a15bb2-3939-422b-aca5-49343d9b22cc.png)
![image](https://user-images.githubusercontent.com/51737180/210187260-fcedeaae-1582-487e-b272-fc87992ddc72.png)

Figure 45 and 46

![image](https://user-images.githubusercontent.com/51737180/210187268-d7108218-29fd-4a0d-a6ea-bd9e464d81b0.png)

Figure 47

## Conclusion
To conclude, we can say that in most cases small numbers of segments in the SLIC algorithm can help the merging algorithms better. This is because of the smaller the superpixels, the more variance the mean of the superpixels. Therefore, large numbers of segments make the merging hard and lead them to more segments even after merging. Consequently, we prefer a small number of segments and the average value for compactness. Moreover, between SLIC and Adaptive version of SLIC, the results in the Adaptive SLIC section, shows that with the same number of segments, SLIC overcomes the adaptive version in terms of not crossing the boundaries. This has been discussed in detail in the Adaptive SLIC section. Besides, the Adaptive version does not work well with the low number of segments and crosses the boundaries frequently. 
For the merging algorithm, experiments show that hierarchical merging works better since the final number of segments is as it is expected, but on some occasions, Ncuts fails to merge to the proper number of segments. Nevertheless, Ncuts is better at adherence to the boundaries. To conclude, each of the algorithms has its pros and cons, and based on the application and our priority we can choose each of them or use state-of-the-art algorithms.












