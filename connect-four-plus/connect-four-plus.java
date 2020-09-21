import javax.swing.*; //Important ability to create Java GUI components
import java.awt.*; //Abstract Window Toolkit for platform-independent windowing and graphics (precedes Swing) 
import java.awt.event.*; 

class connectFour //Starting main Class file
{
  static int[][] board = new int[6][7]; //Creating static variable of board
  static //Intializing every element of board as 0
  {
    for (int i = 0; i < 6; i++)
    {
      for (int j = 0; j < 7; j++)
        board[i][j] = 0;
    }
  }
  
  static double totalTime = 0; //Total amount of time taken
  static double startTime; //The start time of the player's turn in milliseconds
  static double endTime; //The end time of the player's turn in milliseconds
  static double noTime = 0; //The total number of player's turns 
  static int counter; //Creating int variable to determine if it's user or computer turn (even is player, odd is computer)
  
  static JFrame gameWindow; //Creating main frame for entire program
  static JPanel mainPanel; //Creating panel that displays the message
  static JPanel columnPanel; //Creating panel that displays buttons
  static gridGraphics gameBoard; //Creates custom panel that displays Connect 4 board
  
  //static JLabel scoreLabel; //Creates a panel that displays the current score for player
  static JLabel moveLabel; //Creates a panel that displays the moves taken for the player
  static JLabel timeLabel; //Creates a panel that displays the moves taken for the player
  static int moves = 0; //Creates int that is the number of moves by the player
  
  static JButton column1; //Creates button for each column of gameboard
  static JButton column2;
  static JButton column3;
  static JButton column4;
  static JButton column5;
  static JButton column6;
  static JButton column7;
  
  static JFrame startFrame; //Creating frame for asking which user to start

  static JFrame endFrame; //Intializing end JFrame to display Play Again or Exit Program options
  static JLabel endMessage; //Intializing message to say whether player of computer has won
  static JLabel endMoveLabel; //Intializing number of moves taken by player
  static JLabel endTimeLabel; //Intializing average time taken by player
  
  static Boolean win; //Creating Boolean variable returning true if there is a win and false if there is not
  
  //static JPanel buttonsPanel;
  static JButton restart; //Intializing restart button that restarts the program

  public static void main(String args[]) //Starting main method
  {
    startFrame = new JFrame("Play Connect 4!"); //Intializing start frame and setting the title
    startFrame.setSize(440, 75); //Setting the size
    startFrame.setResizable(false); //It cannot be resized by user
    startFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); //It will exit upon closing 
    
    JLabel startMessage = new JLabel("Who will start first?"); //Creating the question label for the starting frame
    startMessage.setFont(new Font("Courier New", Font.BOLD, 14)); //Changing font type and size
    startMessage.setForeground(Color.BLUE); //Changing font colour
    JButton playerSelect = new JButton("You, the Player"); //Creating button to select player
    playerSelect.addActionListener(new playerSelectListener()); //Creating listener for player
    JButton computerSelect = new JButton("The Computer"); //Creating button to select computer
    computerSelect.addActionListener(new computerSelectListener()); //Creating listener for computer
    
    startFrame.add(startMessage); //Adding each component to startFrame
    startFrame.add(playerSelect); //Adding button that selects player
    startFrame.add(computerSelect); //Adding button that selects computer
    startFrame.setLayout(new FlowLayout()); //Intializing layout as Flow
    startFrame.setVisible(true); //Making it visible to the screen
    
    gameWindow = new JFrame("Play Connect 4!"); //Intializing main frame of game and setting the title
    gameWindow.setSize(710, 700); //Setting the size
    gameWindow.setResizable(false); //It cannot be resized by user
    gameWindow.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); //It will exit upon closing
    
    gameBoard = new gridGraphics(); //Intializing the custom graphics panel to display the game board
    
    column1 = new JButton("Column 1"); //Intializing buttons to select which column to drop the tile, setting it to specific dimensions, then intializing a listener for it
    column1.setPreferredSize(new Dimension(125, 25));
    column1.addActionListener(new clickButtonListener1());
    column2 = new JButton("Column 2");
    column2.setPreferredSize(new Dimension(125, 25));
    column2.addActionListener(new clickButtonListener2());
    column3 = new JButton("Column 3");
    column3.setPreferredSize(new Dimension(125, 25));
    column3.addActionListener(new clickButtonListener3());
    column4 = new JButton("Column 4");
    column4.setPreferredSize(new Dimension(125, 25));
    column4.addActionListener(new clickButtonListener4());
    column5 = new JButton("Column 5");
    column5.setPreferredSize(new Dimension(125, 25));
    column5.addActionListener(new clickButtonListener5());
    column6 = new JButton("Column 6");
    column6.setPreferredSize(new Dimension(125, 25));
    column6.addActionListener(new clickButtonListener6());
    column7 = new JButton("Column 7");
    column7.setPreferredSize(new Dimension(125, 25));
    column7.addActionListener(new clickButtonListener7());
    
    columnPanel = new JPanel(); //Intializing the upper panel that displays the buttons to select a column and adding each button to it
    columnPanel.add(column1);
    columnPanel.add(column2);
    columnPanel.add(column3);
    columnPanel.add(column4);
    columnPanel.add(column5);
    columnPanel.add(column6);
    columnPanel.add(column7);
    columnPanel.setLayout(new BoxLayout(columnPanel,BoxLayout.X_AXIS)); //Setting it as Box layout, so no spaces
    
    restart = new JButton("Restart Game");
    restart.addActionListener(new restartButtonListener());

    mainPanel = new JPanel(); //Intializing main panel that will display the dialogue  
    timeLabel = new JLabel("Your Time Taken: 0 s  "); //Intializing time label that displays the time taken
    timeLabel.setFont(new Font("Courier New", Font.BOLD, 13)); //Intializing font type and size
    timeLabel.setForeground(Color.BLUE); //Intializing font colour
    moveLabel = new JLabel("Your Moves Made: 0  "); //Creating move label displaying number of moves
    moveLabel.setFont(new Font("Courier New", Font.BOLD, 13)); //Intializing font type and size
    moveLabel.setForeground(Color.BLUE); //Intializing font colour
    
    mainPanel.add(moveLabel); //Adds move label to the main panel
    mainPanel.add(timeLabel); //Adds time label to the main panel
    mainPanel.add(restart); //Adding restart button to the main panel
    mainPanel.setLayout(new FlowLayout()); //Intializing main panel with flow layout
    
    gameWindow.setLayout(new BorderLayout()); //Setting the layout as Border layout
    gameWindow.add(columnPanel, BorderLayout.NORTH); //Setting the button panel on top
    gameWindow.add(gameBoard, BorderLayout.CENTER); //Setting the game board in the middle
    gameWindow.add(mainPanel, BorderLayout.SOUTH); //Adding the main panel to the bottom of the main frame
    
    endMessage = new JLabel(); //Intializing end message label wihtout prelimeray text
    endMessage.setFont(new Font("Courier New", Font.BOLD, 13)); //Changing font type and size
    endMessage.setForeground(Color.BLUE); //Intializing font colour
    endMoveLabel = new JLabel(); //Intializing end move message label wihtout prelimeray text
    endMoveLabel.setFont(new Font("Courier New", Font.BOLD, 13)); //Changing font type and size
    endMoveLabel.setForeground(Color.BLUE); //Intializing font colour
    endTimeLabel = new JLabel(); //Intializing end time message label wihtout prelimeray text
    endTimeLabel.setFont(new Font("Courier New", Font.BOLD, 13)); //Changing font type and size
    endTimeLabel.setForeground(Color.BLUE); //Intializing font colour
  }
  
  static class playerSelectListener implements ActionListener //Listener if the user chooses player to go first
  {  
    public void actionPerformed(ActionEvent event) //What to do...
    {     
      counter = 1; //Counter will be 1, since player is going first
      startFrame.setVisible(false); //Hiding start frame since a selection was made
      gameWindow.setVisible(true); //Making the main frame visible
      
      startTime = (System.currentTimeMillis())/1000; //Gets the current time
    }
  }
  
  static class computerSelectListener implements ActionListener //Listener if the user chooses computer to go first
  {  
    public void actionPerformed(ActionEvent event) //What do to...
    {     
      counter = 2; //Counter will be 2, since computer is going first
      startFrame.setVisible(false); //Hiding start frame since a selection was made
      gameWindow.setVisible(true); //Making the main frame visible
      
      tileAdder(AI(board) + 1); //Calling the AI method to make its move
      //win = winCheck(board);
    }
  }
  
  static class clickButtonListener1 implements ActionListener //Creating a listener if the user selects column X to drop a tile
  {  
    public void actionPerformed(ActionEvent event) //What to do...
    {     
      if (board[0][0] == 0) //Only execute if the top row isn't occupied
        buttonAction(1); //Calling button action method that's common to all buttons below to execute specific commands
    }
  }
  
  static class clickButtonListener2 implements ActionListener //Please see above
  {  
    public void actionPerformed(ActionEvent event)  
    {     
      if (board[0][1] == 0)
        buttonAction(2);
    }
  }
  
  static class clickButtonListener3 implements ActionListener //Please see above
  {  
    public void actionPerformed(ActionEvent event)  
    {     
      if (board[0][2] == 0)
        buttonAction(3);
    }
  }

  static class clickButtonListener4 implements ActionListener //Please see above
  {  
    public void actionPerformed(ActionEvent event)  
    {     
      if (board[0][3] == 0)
        buttonAction(4);
    }
  }
  
  static class clickButtonListener5 implements ActionListener //Please see above
  {  
    public void actionPerformed(ActionEvent event)  
    {     
      if (board[0][4] == 0)
      {
        buttonAction(5);
      }
    }
  }
  
  static class clickButtonListener6 implements ActionListener //Please see above
  {  
    public void actionPerformed(ActionEvent event)  
    {     
      if (board[0][5] == 0)
        buttonAction(6);
    }
  }
  
  static class clickButtonListener7 implements ActionListener //Please see above
  {  
    public void actionPerformed(ActionEvent event)  
    {     
      if (board[0][6] == 0)
        buttonAction(7);
    }
  }
  
  static class restartButtonListener implements ActionListener  //Restart button listener...
  {  
    public void actionPerformed(ActionEvent event) //What to do...
    {     
      moves = 0; //Reset move as 0 because the game is restarting
      totalTime = 0; //Reset total time as 0 because game is restarting
      moveLabel.setText("Your Moves Made: " + moves + "  "); //Resetting move label text with updated move amount which is 0
      moveLabel.revalidate(); //Saving the label changes
      
      //Intializing every element of the board array as 0 because game is restarting
      for (int i = 0; i < 6; i++)
      {
        for (int j = 0; j < 7; j++)
          board[i][j] = 0;
      }
      
      gameWindow.setVisible(false); //Hiding the game window
      startFrame.setVisible(true); //Showing the start window where user can choose who will begin
    }
  }

  static class gridGraphics extends JPanel //Creating custom panel that displays the game board
  {
    public void paintComponent(Graphics g) //Adding a graphics component called g
    { 
      super.paintComponent(g); //Prints the component
      g.setColor(Color.BLUE); //Sets g as color blue
      g.fillRect(0, 0, 700, 600); //Creating blue background for game board
      
      g.setColor(Color.RED); //Setting g as red
      for (int i = 1; i <= 7; i++) //Creating red vertical grid lines
        g.drawLine((i * 100), 0, (i * 100), 600);
      for (int i = 1; i <= 6; i++) //Creating red horizontal grid lines
        g.drawLine(0, (i * 100), 700, (i * 100));
      
      //If the element of the game board array is a 1 or 2, display the appropriately-colored tile
      for (int j = 0; j < 7; j++)
      {
        for (int i = 0; i < 6; i++)
        {
          if (board[i][j] == 1) //If it is 1, or computer's tile
          {
            g.setColor(Color.GREEN); //Paint a green cirlce with a radius of 100
            g.fillOval((j * 100), (i * 100), 100, 100);
          }
          else if (board[i][j] == 2) //If it is a 2, or player's tile
          {
            g.setColor(Color.ORANGE); //Paint an orange circle with a radius of 100
            g.fillOval((j * 100), (i * 100), 100, 100);
          }
          else if (board[i][j] == 3) //If it is a 3, or a winning tile
          {
            g.setColor(Color.PINK); //Paint an orange circle with a radius of 100
            g.fillOval((j * 100), (i * 100), 100, 100);
          }
        }
      }
      
      win = winCheck(board); //Checking for a win
      if (win) //If win returns a true
      {
        //Removing everything from main panel
        mainPanel.remove(timeLabel);
        mainPanel.remove(moveLabel);
        mainPanel.remove(restart);
        
        //Adding all ending labels to main panel
        mainPanel.add(endMessage);
        mainPanel.add(endMoveLabel);
        mainPanel.add(endTimeLabel);
        
        //Disablign column buttons so user cannot make another move
        column1.setEnabled(false);
        column2.setEnabled(false);
        column3.setEnabled(false);
        column4.setEnabled(false);
        column5.setEnabled(false);
        column6.setEnabled(false);
        column7.setEnabled(false);
        
        //Saving changes made to main panel and then repainting the game window
        mainPanel.revalidate();
        gameWindow.repaint();   
        
        endFrame = new JFrame("What do to next?"); //Setting title of the end frame
        endFrame.setSize(250, 70); //Setting the size
        endFrame.setResizable(false); //It cannot be resized by user
        endFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); //It will exit upon closing 
        
        JButton yesButton = new JButton("Play Again!"); //Intializing yes button to Play Again
        yesButton.addActionListener(new yesButtonListener()); //Intializing a button listener
        JButton noButton = new JButton("Exit Program!"); //Intializing no button to Exit Program
        noButton.addActionListener(new noButtonListener()); //Intializing a button listener
        
        //Adding buttons to the end frame, setting it as flow layout then making it visible
        endFrame.add(yesButton); 
        endFrame.add(noButton);
        endFrame.setLayout(new FlowLayout());
        endFrame.setVisible(true);
      }
    }
  }
  
  static class yesButtonListener implements ActionListener //Intializing yes button listener
  {  
    public void actionPerformed(ActionEvent event)  
    {     
      //Setting game window and end frame as false because program will restart
      gameWindow.setVisible(false);
      endFrame.setVisible(false);
      
      //Enabling all the disabled column buttons again
      column1.setEnabled(true);
      column2.setEnabled(true);
      column3.setEnabled(true);
      column4.setEnabled(true);
      column5.setEnabled(true);
      column6.setEnabled(true);
      column7.setEnabled(true);
      
      moves = 0; //Intializing moves as 0 because program has restarted
      totalTime = 0; //Intializing total time as 0 because program has restarted
      
      //Removing end messages from main panel
      mainPanel.remove(endMessage);
      mainPanel.remove(endMoveLabel);
      mainPanel.remove(endTimeLabel);
      
      //Setting the standard labels for first time 
      moveLabel.setText("Your Moves Made: 0  ");
      timeLabel.setText("Your Time Taken: 0 s  ");
      
      //Intializing every element of board array as 0  
      for (int i = 0; i < 6; i++)
      {
        for (int j = 0; j < 7; j++)
          board[i][j] = 0;
      }
      
      //Adding back the standard labels to main panel, saving it then making the start frame visible again
      mainPanel.add(moveLabel);
      mainPanel.add(timeLabel);
      mainPanel.add(restart);
      mainPanel.revalidate();
      startFrame.setVisible(true);
    }
  }
  
  static class noButtonListener implements ActionListener //Intializing no button listener
  {  
    public void actionPerformed(ActionEvent event)  
    {     
      gameWindow.setVisible(false); //Hiding game window
      endFrame.setVisible(false); //Hiding end frame
    }
  }
  
  public static void buttonAction(int num) //Intializing button listeners for column buttons
  {
    endTime = (System.currentTimeMillis())/1000; //CLARENCE!!!! getting the end time
    totalTime += (endTime - startTime); //CLARENCE!!!! adding on to the total time by subtracting start time from end time
    noTime += 1; //Increasing number of times by 1
    
    gameWindow.repaint(); //Repainting the main frame
    tileAdder(num); //Giving the column selection to tileAdder method that'll accordingly change the game board array
    turnChanger(counter); //Changes the dialogue to the other
    
    moves++; //Increasing number of moves by 1
    //Removing time and move labels and restart button
    mainPanel.remove(timeLabel);
    mainPanel.remove(moveLabel);
    mainPanel.remove(restart);
    
    timeLabel.setText("Your Time Taken: " + ((endTime - startTime)/1000000) + " s  "); //Setting the time label to display the time
    
    moveLabel.setText("Your Moves Made: " + moves + "  "); //Setting the move label to display the moves
    
    //Adding move label, time label and restart button back to main panel
    mainPanel.add(moveLabel); 
    mainPanel.add(timeLabel);
    mainPanel.add(restart);
        
    mainPanel.revalidate(); //Update the change
    mainPanel.repaint(); //Repaint the main panel
  }
  
  public static void tileAdder(int choice) //Method to determine which element of the game board array will be changed
  {
    for (int i = 5; i >= 0; i--) //Loop from bottom of selected column to the top
    {
      if (board[i][choice - 1] == 0 && counter % 2 != 0) //If an element is empty and the counter is odd 
      {
        board[i][choice - 1] = 1; //Change element value to 1
        counter++; //Increase counter by 1
        break; //Break out of loop because element was successfully changed
      }
      else if (board[i][choice - 1] == 0 && counter % 2 == 0) //If an element is empty and the counter is even
      {
        board[i][choice - 1] = 2; //Change element value to 2
        counter++;
        break; //Break out of loop because element was successfully changed
      }
    }
  }
  
  public static void turnChanger(int counter) //Method to execute for whether the player or computer will go next
  {
    if (counter % 2 == 1) //If the counter is even or it's the player
    {
      moves++; //Increasing number of moves by one
      mainPanel.remove(moveLabel); //Removing the moves label
      
      moveLabel.setText("Your Moves Made: " + moves + "  "); //Setting the move label to current number of moves
      mainPanel.add(moveLabel); //Add the updated move label
      
      mainPanel.revalidate(); //Update the change
      mainPanel.repaint(); //Repaint the main panel
      
      startTime = (System.currentTimeMillis())/1000; //Gets the current time
    }
    else
    {      
      tileAdder(AI(board) + 1); //Have the AI go
    }
  } 
  
  public static int AI(int[][] board) { //AI method that returns which column it wants to place its disk
    
    int[][] boardCopy = board; //make a copy of the board so anything we change wont affect the actual board
    
    int[] scoring = new int[7]; //make array to keep track of scores
    int bestOptionScore = -10000000; //make the best option's score
    int bestOption = 3; //make the best option's index, usually the middle column is the best sooo set it to 3
    
    scoring[0] = 0; //initialize that certain columns are generally better than others
    scoring[1] = 1;
    scoring[2] = 2;
    scoring[3] = 3;
    scoring[4] = 2;
    scoring[5] = 1;
    scoring[6] = 0;
      
//////////   //Check if it were to make a move there, will it win
    for (int choice = 0; choice < 7; choice++) { //for loop for columns
      for (int spot = 5; spot >= 0; spot--){ // for loop for rows
        if (boardCopy[spot][choice] == 0) { //check if slot if empty
          boardCopy[spot][choice] = 2; //fill spot with piece
          
          int hwin = hcheck(boardCopy);
          int vwin = vcheck(boardCopy);
          int dwin = dcheck(boardCopy);
          
          if (dwin == 2|| hwin == 2 || vwin == 2) {
            scoring[choice] = 100000000;
          }
          
          boardCopy[spot][choice] = 0; //fill spot with piece
          
          break; //break out of for loop
        } // end if
      } //end row
    } //end column
    
//////////   //Check if it moves there, will it lose next move with multiple depths (3)
    for (int choice = 0; choice < 7; choice++) { //for loop for columns
      for (int spot = 5; spot >= 0; spot--){ // for loop for rows
        if (boardCopy[spot][choice] == 0) { //check if slot if empty
          
          boardCopy[spot][choice] = 2; //fill spot with piece
          
          for (int column = 0; column <7; column++) {
            for (int row = 5; row >= 0; row--){ // for loop for rows
              if (boardCopy[row][column] == 0) {
                
                boardCopy[row][column] = 1; //fill spot with piece
                
                int hwin = hcheck(boardCopy); //check if computer will lose
                int vwin = vcheck(boardCopy);
                int dwin = dcheck(boardCopy);
                
                if (dwin == 1|| hwin == 1 || vwin == 1) {
                  scoring[choice] -= 1000; //adjust score accordingly
                }
                
                for (int column1 = 0; column1 <7; column1++) {
                  for (int row1 = 5; row1 >= 0; row1--){ // for loop for rows
                    if (boardCopy[row1][column1] == 0) {
                      
                      boardCopy[row1][column1] = 2; //fill spot with piece
                      
                      for (int column2 = 0; column2 <7; column2++) {
                        for (int row2 = 5; row2 >= 0; row2--){ // for loop for rows
                          if (boardCopy[row2][column2] == 0) {
                            
                            boardCopy[row2][column2] = 1; //fill spot with piece
                            
                            int hwin1 = hcheck(boardCopy);
                            int vwin1 = vcheck(boardCopy);
                            int dwin1 = dcheck(boardCopy);
                            
                            if (dwin1 == 1|| hwin1 == 1 || vwin1 == 1) {
                              scoring[choice] -= 1000;
                            }
                            for (int column3 = 0; column3 <7; column3++) {
                              for (int row3 = 5; row3 >= 0; row3--){ // for loop for rows
                                if (boardCopy[row3][column3] == 0) {
                                  
                                  boardCopy[row3][column3] = 2; //fill spot with piece
                                  
                                  for (int column4 = 0; column4 <7; column4++) {
                                    for (int row4 = 5; row4 >= 0; row4--){ // for loop for rows
                                      if (boardCopy[row4][column4] == 0) {
                                        boardCopy[row4][column4] = 1; //fill spot with piece
                            
                                        int hwin2 = hcheck(boardCopy);
                                        int vwin2 = vcheck(boardCopy);
                                        int dwin2 = dcheck(boardCopy);
                                        
                                        if (dwin2 == 1|| hwin2 == 1 || vwin2 == 1) {
                                          scoring[choice] -= 1000;
                                        }
                                        
                                        
                                        boardCopy[row4][column4] = 0; //revert

                                        break;
                                      }
                                    }
                                  }
                                  
                                  boardCopy[row3][column3] = 0; //revert
                                  break;
                                }
                              }
                            }
                            
                            boardCopy[row2][column2] = 0; //revert
                            
                            break;
                          }
                        }
                      }
                      
                      boardCopy[row1][column1] = 0; //revert
                      
                      break;
                    }
                  }
                }
                
                boardCopy[row][column] = 0; //revert
                
                break;
              }
            }
          }
          
          boardCopy[spot][choice] = 0; //fill spot with piece
          
          break; //break out of for loop
        } // end if
      } //end row
    } //end column

    for (int i = 0; i<7; i++) { //check which column move is possible
      boolean lineChecker = lineCheck(board, i);
      if (lineChecker == true)
        scoring[i] = -1000000000;

    }
    for (int i = 0; i<7; i++) { //check which column has the highest score
      if (scoring[i] > bestOptionScore) { //compares the score in each column ro find the highest value
        bestOptionScore = scoring[i]; //if the score in that column is higher than the current best, it becomes the new best
        bestOption = i; //change the best option to the one that will outcome the highest win score
      } 
    }
    return bestOption; //return the best column position
  }
  
  //method to check if a vertical line is full of pieces
  public static boolean lineCheck(int board[][], int i)
  {
    boolean check = false;  //boolean value to check if line is full
    if(board[0][i] != 0)  //checking the top row positions
      check = true;  //boolean value is true if the line is full
    return check;
  }
  
  //method to check for horizontal wins
  public static int hcheck(int board[][])
  {  //import the board
    int check = 0;  //boolean value to check for wins
    for(int row = 0; row < 6; row++)
    {
      for(int column = 0; column < 4; column++)
      {
        if(board[row][column] != 0 && board[row][column] == board[row][column + 1] && board[row][column] == board[row][column + 2] && board[row][column] == board[row][column + 3])  //when the position has something and is equal to the next column position
          check = board[row][column];  //check for wins is true
      }
    }
    return check;
  }
        
  //method to check for vertical wins
  public static int vcheck(int board[][])
  {  //import the board
    int check = 0;  //boolean value to check for wins
    for(int row = 0; row < 3; row++)
    {
      for(int column = 0; column < 7; column++)
      {
        if(board[row][column] != 0 && board[row][column] == board[row + 1][column] && board[row][column] == board[row + 2][column] && board[row][column] == board[row + 3][column])  //when the position has something and is equal to the position below
          check = board[row][column];  //check for wins is true
      }
    }
    return check;
  }
  
  //method to check for diagonal wins
  public static int dcheck(int board[][])
  {  //import the board
    int check = 0;  //boolean value to check for wins
    for(int row = 0; row < 3; row ++)
    {
      for(int column = 0; column < 4; column++)
      {
        if(board[row][column] != 0 && board[row][column] == board[row + 1][column + 1] && board[row][column] == board[row + 2][column + 2] && board[row][column] == board[row + 3][column + 3])  //checking if there are 4 pieces equal diagonally from top left to bottom right
        {
           check = board[row][column];  //check for wins is true
           /*
           board[row][column] = 3;
           board[row + 1][column + 1] = 3;
           board[row + 2][column + 2] = 3;
           board[row + 3][column + 3] = 3;
           */
        }
       }
    }
    
    for(int row = 0; row < 3; row++){
      for(int column = 6; column > 2; column--)
      {
        if(board[row][column] != 0 && board[row][column] == board[row + 1][column - 1] && board[row][column] == board[row + 2][column - 2] && board[row][column] == board[row + 3][column - 3])  //checking if there are 4 pieces equal diagonally from top right to bottom left
          check = board[row][column];  //check for wins is true
      }
    }
    return check;
  }
 
  public static Boolean winCheck(int[][] board) //Method to check for a win
  {
    int hwin = hcheck(board);
    int vwin = vcheck(board);
    int dwin = dcheck(board);
    
    if (dwin == 1 || hwin == 1 || vwin == 1)
    {
      //Setting messages for if computer is the winner
      endMessage.setText("You beat the computer! ");
      endMoveLabel.setText("No. of moves taken: " + moves + " "); //Total number of moves
      endTimeLabel.setText("Average time taken: " + ((totalTime/noTime)/1000000000) + " s "); //Average time
      winningDiscColorChanger(board); //Changing values of winning tiles to 3
      return true; //Return true
    }
    else if (dwin == 2|| hwin == 2 || vwin == 2)
    {
      //Setting messages for if player is the winner
      endMessage.setText("The computer beat you! ");
      endMoveLabel.setText("No. of moves taken: " + moves + " "); //Total number of moves
      endTimeLabel.setText("Average time taken: " + ((totalTime/noTime)/1000000000) + " s "); //Average time
      winningDiscColorChanger(board); //Changing values of winning tiles to 3
      return true; //Return true
    }
    else
      return false; //Returns false if no win is detected
  }
  
  public static void winningDiscColorChanger (int [][] board) {
    for(int row = 0; row < 6; row++) { //horizontal check
      for(int column = 0; column < 4; column++) {
        if(board[row][column] != 0 && board[row][column] == board[row][column + 1] && board[row][column] == board[row][column + 2] && board[row][column] == board[row][column + 3]){  //when the position has something and is equal to the next column position
           board[row][column] = 3;
           board[row][column + 1] = 3;
           board[row][column + 2] = 3;
           board[row][column + 3] = 3;
        }
      }
    }
    
    for(int row = 0; row < 3; row++) { //vertical check
      for(int column = 0; column < 7; column++) {
        if(board[row][column] != 0 && board[row][column] == board[row + 1][column] && board[row][column] == board[row + 2][column] && board[row][column] == board[row + 3][column]) { //when the position has something and is equal to the position below
          board[row][column] = 3;
          board[row + 1][column] = 3;
          board[row + 2][column] = 3;
          board[row + 3][column] = 3;
        }
      }
    }
    
    for(int row = 0; row < 3; row ++) { //diagonal check
      for(int column = 0; column < 4; column++) {
        if(board[row][column] != 0 && board[row][column] == board[row + 1][column + 1] && board[row][column] == board[row + 2][column + 2] && board[row][column] == board[row + 3][column + 3]) { //checking if there are 4 pieces equal diagonally from top left to bottom right
          
          board[row][column] = 3;
          board[row + 1][column + 1] = 3;
          board[row + 2][column + 2] = 3;
          board[row + 3][column + 3] = 3;
          
        }
      }
    }
    
    for(int row = 0; row < 3; row++){
      for(int column = 6; column > 2; column--)
      {
        if(board[row][column] != 0 && board[row][column] == board[row + 1][column - 1] && board[row][column] == board[row + 2][column - 2] && board[row][column] == board[row + 3][column - 3]) { //checking if there are 4 pieces equal diagonally from top right to bottom left
          board[row][column] = 3;
          board[row + 1][column - 1] = 3;
          board[row + 2][column - 2] = 3;
          board[row + 3][column - 3] = 3;
        }
      }
    }
  }
}