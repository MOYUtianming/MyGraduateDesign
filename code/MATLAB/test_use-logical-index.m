scores = [1,2,4,5,1,20,8];
% highscores is a logical index;
highscores = scores > 4;
% use logical index can find the corresponding elements in original
% dataset;
buf = scores(highscores);