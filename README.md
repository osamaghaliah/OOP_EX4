# Pokemon Game:
<div style="width:250px;max-width:100%;"><div style="height:0;padding-bottom:69.2%;position:relative;"><iframe width="250" height="173" style="position:absolute;top:0;left:0;width:100%;height:100%;" frameBorder="0" src="https://imgflip.com/embed/60jys4"></iframe></div><p><a href="https://imgflip.com/gif/60jys4">via Imgflip</a></p></div>

__Game Implementation:__
* __Algorithms:__
      <br>*In terms of algorithms, we managed to implement a graph by using 3 dictionaries - first dictionary was made for vertices, second dictionary was made for the edges that are
      going inside a specified vertex and the third dictionary was made for the edges that are going outside a specified vertex.
      We were requested to implement various functions that are considered a strong tool that contribute to ease for us the way we implement the whole problem - Directed               Weighted
      Graph Implementation.*<br />
     
* __Classes:__
      <br>*In terms of classes, we implemented a customized class for one node of a graph called Vertex, it has 4 attributes: Key - presents the number of a single node in a graph,
      EdgesGoingInside - a dictionary that presents the whole edges that are directed into the node, EdgesGoingOutside - a dictionary that presents the whole edges that are
      directed outside the node. In addition, we implemented the classes that we were told to implement - DiGraph & GraphAlgo that have their own interfaces. We worked according
      to their interface of course and implemented each function that existed in them interfaces.*<br />
      
* __Essential Functions:__
      <br>*The project has 5 essential functions:<br />
            <br>1) Shortest Path.<br />
            <br>2) Save.<br />
            <br>3) Load.<br />
            <br>4) TargetedNode*<br />
       
* __Tests:__
      <br>*For every single function that was implemented in the project, we managed to make tests for them - which asserts if our work actually does work or not.*<br />
      
* __PYGAME:__
      <br>*PYGAME library was used for the GUI. We had a built one from the lecturer, and we adding some customization for it.
      PYGAME's window include the following: Nodes, Edges, Agents & Pokemons.
      The Agents must be eating the Pokemons using paths that should lead him to eat the Pokemon as fast as possible.
      For that step, we used shortestPath function in order to let the Agent go through the fastest path that leads him into the Pokemon and eat it.*<br />
      
* __How To Run:__
      <br>*A .jar file was uploaded named: Ex4_Server_v0.0.jar
      After downloading this file, upload to the project. Then, open the terminal and use the follwing command: java -jar Ex4_Server_v0.0.jar
      By doing this step, you will be connected to a local host, then you will have to run student_code.py file.
      Once the whole steps get successfully done - the game must pop up on your screen automatically.*<br />

                  
