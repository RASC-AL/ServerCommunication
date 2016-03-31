#include "ros/ros.h"
#include "std_msgs/String.h"
#include "opencv2/core/core.hpp"
#include "opencv2/core/utility.hpp"
#include "opencv2/imgproc/types_c.h"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <cv_bridge/cv_bridge.h>
#include <iostream>
#include <cstdlib>

using namespace std;
using namespace cv;



int main(int argc, char **argv)
{
cout<<"ROS works bitches!"<<endl;

// VideoCapture cap(0); // open the default camera
//     if(!cap.isOpened())  // check if we succeeded
//         return -1;

//int h = atoi(argv[1]);
//int l = atoi(argv[2]);

Mat src, hsv, dst;

vector<vector<Point> > contours;
vector<Vec4i> hierarchy;

Scalar blue_low = Scalar(80,110,50);
Scalar blue_high = Scalar(130,255,255);
Scalar red_low = Scalar(170,160,60);
Scalar red_high = Scalar(180,255,255);
Scalar green_low = Scalar(50,90,0);
Scalar green_high = Scalar(75,255,255);


//for(;;){

	

	//cap >> src;
	src = imread("/home/shishir/img4.jpg",1);
	dst = src.clone();

	Mat mask(src.rows,src.cols,CV_8U);

	cvtColor(src, hsv, CV_BGR2HSV);

	vector<Rect> boundRect( 1 );

	//Blue

	inRange(hsv, blue_low, blue_high, mask);

	findContours(mask, contours, hierarchy, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );

	boundRect.resize(contours.size());

	for( int i = 0; i< contours.size(); i++ )
    {
    	boundRect[i] = boundingRect( Mat(contours[i]) );
    	rectangle( dst, boundRect[i].tl(), boundRect[i].br(), Scalar(255,255,255), 2, 8, 0 );
    }

    boundRect.clear();
    contours.clear();

    //Red

	inRange(hsv, red_low, red_high, mask);

	findContours(mask, contours, hierarchy, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );

	boundRect.resize(contours.size());

	for( int i = 0; i< contours.size(); i++ )
    {
    	boundRect[i] = boundingRect( Mat(contours[i]) );
    	rectangle( dst, boundRect[i].tl(), boundRect[i].br(), Scalar(255,255,255), 2, 8, 0 );
    }

    boundRect.clear();
    contours.clear();


    //Green

	inRange(hsv, green_low, green_high, mask);

	findContours(mask, contours, hierarchy, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );

	boundRect.resize(contours.size());

	for( int i = 0; i< contours.size(); i++ )
    {
    	boundRect[i] = boundingRect( Mat(contours[i]) );
    	rectangle( dst, boundRect[i].tl(), boundRect[i].br(), Scalar(255,255,255), 2, 8, 0 );
    }

    boundRect.clear();
    contours.clear();

	namedWindow( "Input Window", WINDOW_NORMAL);
	imshow( "Input Window" ,src );
	namedWindow( "Test Window", WINDOW_NORMAL );
	imshow( "Test Window" , dst );

	waitKey(0);
//}

//VideoCapture::release(cap);
return 0;
}
