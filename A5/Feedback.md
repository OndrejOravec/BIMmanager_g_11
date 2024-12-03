# Group 14 feedback
I really like the idea behind your tool. Essentially, when a third party is verifying the validity of an MEP design, they don’t have to go through the time- and resource-intensive process of creating the MEP design themselves, as the first party does. Instead, they utilize the existing BIM model, using OpenBIM tools to efficiently verify the accuracy of the design proposal.Moreover, as developed tool verify quantities and dimensioning, I see potential in using it for Project management, LCA and Facility Management.

Tutorial is nicely structured, and easy to understand. Comprehensive step-by-step explenation of different script parts is essetnial for users to use your tool in intended manner. Also the fact, that you havent just provided guidance for sciprt itself, but also  for neccesary prerequiesities to make sciprt work, like installing Blender, Bonsai

Stuff to consider: 
Do you think script would be able to handle calculations even when parts constituting for HVAC systems would be defined with different IFCs? For example once I have BIM where everything that consituted for HVAC system was modeled as "IfcParts". Would it be possible to adjust this tool to make it work under such conditions?
Also if flow rates wouldnt be defined in BIM, would user be required for a manual input for this data?

In my opinion, your script is powerful tool with great  potential for real- life applications in construction industry that can be utilized by different stakeholder. Additonaly, simplicity and straightforwadness are positive factorts that can contribute in better adoption of your tool for users with different level of skill in OpenBIM.

# Group 15 feedback
Tool description is super straightforward, clearly conveying it beneftis to the user. Also I believe script is easy to understand even for users who are not familiar with OpenBIM.

Stuff to consider: 
Have you considered calculating the U-value of the entire window system as a weighted average of the U-values of its individual components? For example, you could first calculate the U-value of the glazing (for the window or curtain wall) and then the U-value of the frame. Afterward, you could determine the overall U-value for the entire window system by weighting these values based on the proportion of the glazing and frame areas relative to the total window area.

Script could have a function implemented where it would compare calculated U values with U values required in Standart.

In general, I see this tool as an important and powerful resource that simplifies the process of verifying U-values for building envelopes, which is crucial for ensuring a suitable indoor climate.
