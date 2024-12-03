This file contains individual reflections for assignment A5 of both members of BIM manager group 11. 

# Ondrej Individual Reflection
**My future for Advanced use of OpenBIM:**
- *Are you likely to use OpenBIM tools in your professsional life in the next 10 years?:*

I see a lot of potential for using OpenBIM in my future career in architectural acoustics, rimarily because the nature of this field relies heavily on interdisciplinary collaboration with various professionals within consultancy and effective communication with diverse stakeholders in the construction industry.

Since OpenBIM is collaborative approach to BIM that emphasizes interoperability among above mentioned stakeholders, I believe it is only a matter of time before I encounter situations where I will be able to apply knowledge gained from this course.

Moreover, considering rapid digitalization trends withing construction industry over past years, it seem more likely that I will utilize in someway OpenBIM tools within next 10 years. So yes, I see it very likely I will come acroos situation within next 10 years where I will be working with OpenBIM tools.  

- *Are you likely to use OpenBIM tools in your thesis?:*

Regarding me thesis, Iam already working on my thesis this semester and I havent planned to use any OpenBIM tools. However, Iam still glad that project Magnus and I carried out was related to acoustics which is same topic as my MSc thesis is about, therfore giving me broader knowledge about possibilties of architectural acoustics design.

**Wrap up:**

Thorughout first half of course Magnus and I been more engaged in managerial position, where even though we were in touch with our analaysts and were engaged in their process of design we felt like hanging in air and depended on their otucome or in other words, not contributive as much as we wanted to general development of different tools for Indoor Climate domain. 
Speaking for myself, even though I had some ideas which way to go, I felt I couldnt utilize/ develope them further since I didnt want to be in posistion to tell analysts which way to develop code which they were working most on. 
Also another reason why I felt bit left out was probably that analysts didnt feel need to consult with us much their ideas and general approaches.

After completing the A2 assignment, Magnus and I began discussing the possibility of developing something on our own as managers, focusing on Indoor Climate. I felt that I wasn’t gaining as much from the course as I had hoped, as my role was more about assisting other analyst groups rather than actively engaging in developing my own tool.
So basically in order to increase our learning outcome and gain a deeper understading of involved problematics we decided to focus on developing own script for Indoor Climate domain.
Since we were both with familiar with acoustics, and its importance for satisfactory Indoor Environment we explored possibilites how to carry out task related to acoustic conditions that would be possible to verify in context of provided IFC model, but also claims that owners of IFC model did in their report. We found out they performed some basic calculations for Reverberation Time T for some specific rooms and we decided we can explore this idea further by verifing accuracy of their calculation via implementation of OpenBIM principles and developlment of our own tool.

We started with sketching of workflow programming chart where we brainstormed how this potential script could work and what it should include : https://github.com/OndrejOravec/BIMmanager_g_11/blob/main/A3/BPMN%20diagram.svg This is finalized diagram representing how script works now, but before structure was simplier and more straightforward since we were not that familiar with IFC model complexity. 

Early stage diagam was build on these assumptions : 

- *Sound absoprption of materials defined :* In ideal complexity of IFC model Sound absorption coefficient of finishing layer would be defined. We expected it wont be defined however, as script should be simplest and most straightforward for smoothnes of worfklow and for sake of potential succesful implementation for usage for different users we utilized this approach with assumptions that sound absopriton coefficient is defined. As expected, coefficient was not defined so we incorporated "Decision" function which guides process in two scenarios : if coefficient is defined, it is automatically extracted from the corresponding material of the investigated room ; if it is not defined function prompts user for manual input of coefficient to proceed.

- *Rooms defined :*  - In the early stage, code was built on assumption that IFC model has defined rooms, which is generally more common across various IFC models than having sound absorption coefficient defined. If this assumption had been correct, we could make script work the way that it recognizes fucntion of room by its name tag (meeting room, office room) and subsequently extract volume which is required for calculation of Reveberation Time T. As it turned out that this IFC doenst contain room definition we proceed with approach that script will calculate room volume according its boundaries like walls, slabs and ceiling and calculate volume with bounding box function. Additionally, it was necessary to determine which rooms were relevant for Reverberation Time analysis. Certain rooms, based on their typology, are not suitable for this type of analysis due to their geometry or intended purpose.
  This is simplified explanation, more it is explained in script file from line number 96 "Geometry Settings" : https://github.com/OndrejOravec/BIMmanager_g_11/blob/main/A3/main.py

With all these precautions in place and the IDS defined, I see great potential for implementing our tool in future projects. There is also scope for various improvements to enhance the existing tool, such as: 

*More complex Reverberation time analysis :* There is possibility to develope script futher where for Reverberation Time calculation where it can implement variables such as occupancy, or furnishing.

*Handling more complex geometries :* There are forms of Reverberation formula which are not based on assumption of parralelly oriented walls in cuboid shape rooms, therfore it would be possible make script less constraining and give user more freedom.

In general I enjoyed this course, even though during first half I felt Iam not contributing as much as I wanted. I appreciate possiblity of developing own script even though we decided to do so in later stage of course.


# Magnus Individual Reflection
**My future for Advanced use of OpenBIM:**
- *Are you likely to use OpenBIM tools in your professsional life in the next 10 years?:*

Yes, absolutely. OpenBIM tools encompass some of the aspects of architectural engineering that I enjoy the most, especially their versatility across various topics. My first introduction to tools like Grasshopper and Rhino was during my bachelor’s fagprojekt (subject project), where I discovered my passion for parameterization. While it is complex, I find the idea of developing geometric scripts to aid the early design process fascinating. Such scripts can provide a rough, optimized geometry that architects can refine and build upon.

This approach means we wouldn’t need to start from scratch every time but rather work from a geometrically informed base evaluated against specific parameters. I believe this can significantly enhance the design process.

Even though I’m not the strongest coder, I’ve managed to make progress and improve my skills gradually. For instance, this semester marked my first experience with Blender, and I really appreciate its open-source nature. While Grasshopper requires a Rhino license, which can be a drawback, tools like Blender demonstrate the potential of accessible, powerful software. I’d be surprised if I didn’t incorporate OpenBIM in my future work.

- *Are you likely to use OpenBIM tools in your thesis?:*

I hope so, but it depends on the topic I choose and the supervisor I work with. I have broad interests, including acoustics, ventilation, and aspects of sustainability (although I find the process of conducting LCAs tedious, I enjoy the insights they provide). However, what truly fascinates me is optimizing the early design phase. Historically, buildings have often been designed without analytical tools until the later stages, but this is changing. We are beginning to integrate analysis into the modeling process, which I think is an incredible development. It enables us to create better buildings with more informed decisions from the outset.

An idea I find particularly exciting involves a tool that allows designers to input project parameters—such as the number of rooms, building type, room types and sizes—and upload contextual data like surrounding buildings, trees, and the site’s layout. The tool could then generate hundreds of optimized building layouts with recommended room configurations, floorplans, and window placements. Designers could review the top 5–10 results and use them as inspiration or starting points for further refinement. While I’m not suggesting that architects are “guessing” during design, having this kind of engineering-guided framework early on could significantly improve the final outcome.

To answer the question directly, working on something like this would be impossible without OpenBIM tools. Whether I pursue this exact idea or explore smaller-scale optimizations within another topic, OpenBIM will likely play a critical role in my thesis work.

**Wrap up:**
