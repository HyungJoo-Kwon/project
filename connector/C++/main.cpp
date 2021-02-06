#include <opencv2/opencv.hpp>
#include <iostream>
#include <algorithm>
#include <vector>

using namespace cv;
using namespace std;

void L_putTR(Mat& img)
{
	int x, y, xx, yy;
	x = 30, y = 180, xx = 170, yy = 500;
	int font = FONT_HERSHEY_PLAIN;
	double fontScale = 2;
	rectangle(img, Point(x, y), Point(xx, yy), Scalar(0, 255, 0), 2);
	Point llocation(x - 10, y - 10);
	putText(img, "left_side", llocation, font, fontScale, Scalar(0, 255, 0), 1);
}
void R_putTR(Mat& img)
{
	int x, y, xx, yy;
	x = 30, y = 180, xx = 170, yy = 500;
	int font = FONT_HERSHEY_PLAIN;
	double fontScale = 2;
	Point rlocation(img.cols - xx - 10, y - 10);
	rectangle(img, Point(img.cols - x, y), Point(img.cols - xx, yy), Scalar(0, 255, 0), 2);
	putText(img, "right_side", rlocation, font, fontScale, Scalar(0, 255, 0), 1);
}
void B_putTR(Mat& img)
{
	int font = FONT_HERSHEY_PLAIN;
	double fontScale = 2;
	Point blocation(200, 550 + 30);
	putText(img, "bottom_side", blocation, font, fontScale, Scalar(0,255,0), 1);
	rectangle(img, Point(200, 350), Point(img.cols - 200, 550), Scalar(0, 255, 0), 2);
}


int main()
{
	Mat img_src, img_dst, img_gray;
	img_src = img_dst = imread("images/3번 L50_OK.bmp", IMREAD_COLOR);

	if (img_src.empty())
	{
		cout << "이미지 파일을 읽을 수 없습니다." << endl;
		return -1;
	}
	//size (1295,971)
	pyrDown(img_src, img_src);
	pyrDown(img_dst, img_dst);

	//int height = 480;
	//Mat img(height, width, CV_8UC3);

	Scalar red(0, 0, 255);
	Scalar green(0, 255, 0);
	Scalar blue(255, 0, 0);

	cvtColor(img_src, img_gray, COLOR_BGR2GRAY);
	threshold(img_gray, img_gray, 127, 255, THRESH_BINARY); // 127보다 크면 255로 바꿔라,

	int font = FONT_HERSHEY_PLAIN;
	double fontScale = 2;

	//left,right,bottm side rectangle, text
	int x, y, xx, yy;
	x = 30, y = 180, xx = 170, yy = 500;

	//rectangle(img_dst, Point(x, y), Point(xx, yy), green, 2);
	//Point llocation(x - 10, y - 10);												//left
	//putText(img_dst, "left_side", llocation, font, fontScale, green, 1);

	//Point rlocation(img_src.cols - xx - 10, y - 10);													
	//rectangle(img_dst, Point(img_src.cols - x, y), Point(img_src.cols - xx, yy), green, 2);		//right
	//putText(img_dst, "right_side", rlocation, font, fontScale, green, 1);

	//rectangle(img_dst, Point(200, 350), Point(img_src.cols - 200, 550), green, 2); // bottom
	//Point blocation(200, 550 + 30);
	//putText(img_dst, "bottom_side", blocation, font, fontScale, green, 1);


	int iteration = 5;
	Mat kernel = getStructuringElement(MORPH_RECT, Size(3, 3));
	morphologyEx(img_gray, img_gray, MORPH_CLOSE, kernel, Point(-1, -1), iteration);

	Rect lrect(30, 180, 140, 320);
	Rect brect(180, 380, 895, 200);
	Rect rrect(1125, 180, 140, 320);

	Mat img_gray_left, img_gray_bottom, img_gray_right;
	img_gray_left = img_gray(lrect);
	img_gray_bottom = img_gray(brect);
	img_gray_right = img_gray(rrect);

	vector<vector<Point> > contours_bottom;
	vector<vector<Point> > contours_left;
	vector<vector<Point> > contours_right;
	vector<vector<Point> > contours;
	findContours(img_gray_bottom, contours_bottom, RETR_LIST, CHAIN_APPROX_SIMPLE);
	findContours(img_gray_left, contours_left, RETR_LIST, CHAIN_APPROX_SIMPLE);
	findContours(img_gray_right, contours_right, RETR_LIST, CHAIN_APPROX_SIMPLE);
	findContours(img_gray, contours, RETR_LIST, CHAIN_APPROX_SIMPLE);

// ===================================================================================================================	
	int bottom_count = 0;
	for (size_t i = 0; i < contours_bottom.size(); i++)			// bottom
	{
		drawContours(img_gray_bottom, contours_bottom, i, green, 5);

		int area = contourArea(contours_bottom[i]);

		bottom_count = i;	
	}
	
	for (size_t i = 0; i < contours_bottom.size(); i++)			// bottom
	{
		drawContours(img_gray_bottom, contours_bottom, i, green, 5);

		int area = contourArea(contours_bottom[i]);

		if (bottom_count < 3)
		{
			rectangle(img_dst, Point(200, 180), Point(1100, 500), red, 2);
			Point location(img_dst.cols / 2 - 100, img_dst.rows / 2 + 300);
			putText(img_dst, "FAIL : REVERSE PRINTING", location, FONT_HERSHEY_PLAIN, 3, red, 1);
			break;
		}
		if (area < 2200)
		{
			Rect rect = boundingRect(contours[i]);
			rectangle(img_dst, rect, red, 2);
			Point location(img_dst.cols / 2 - 100, img_dst.rows / 2 + 300);
			putText(img_dst, "FAIL : PRINTING ERROR", location, FONT_HERSHEY_PLAIN, 3, red, 1);

			
		}

		else
		{
			B_putTR(img_dst);
			cout << i << ":" << area << endl;
			Point aaa = contours[i][0];
			Point location1(aaa.x, aaa.y);
			string strlocation1 = "X:" + to_string(aaa.x) + ", Y:" + to_string(aaa.y);
			Point location2(aaa.x, aaa.y - 10);
			string strlocation2 = "Area: " + to_string(area);
			putText(img_dst, strlocation1, location1, FONT_HERSHEY_PLAIN, 1, green, 1);
			putText(img_dst, strlocation2, location2, FONT_HERSHEY_PLAIN, 1, green, 1);

			Moments mu;
			mu = moments(contours[i]);
			int cx = static_cast<float> (mu.m10 / (mu.m00 + 1e-5));
			int cy = static_cast<float> (mu.m01 / (mu.m00 + 1e-5));
			circle(img_dst, Point(cx, cy), 5, blue, -1);
			Point mulocation(cx + 10, cy);
			putText(img_dst, to_string(i), mulocation, FONT_HERSHEY_PLAIN, 1, blue, 1);
		}
	}
	// ===================================================================================================================	
	int right_count = 0;
	vector<int> right_check;
	for (size_t i = 0; i < contours_right.size(); i++)			// right
	{
		drawContours(img_gray_bottom, contours_right, i, green, 5);
		int area = contourArea(contours_right[i]);
		
		cout << i << ":" << area << endl;
;
		if (right_count < i)
			right_count = i;
		if(area < 3000)
			right_check.push_back(i);
	}
	if (right_count <=3)
	{
		for (auto i = 0; i < right_check.size(); i++)
		{
			Rect rect = boundingRect(contours_right[i]);
			Point pt  (1125, 180);
			rect = rect + pt;
			/*new rect = 1125, 180, 140, 320*/
			rectangle(img_dst, rect, red, 2);
		}
		Point location(img_dst.cols / 2 - 100, img_dst.rows / 2 + 300);
		putText(img_dst, "FAIL : BLOCKED HOLL", location, FONT_HERSHEY_PLAIN, 3, red, 1);
	}
	else
	{
		R_putTR(img_dst);
		for (size_t i = 0; i < contours_right.size(); i++)									//right
		{
			drawContours(img_gray_right, contours_left, i, green, 5);
			int area = contourArea(contours_right[i]);
			Point aaa = contours_right[i][0];
			aaa.x += 1125;
			aaa.y += 180;
			Point location1(1125, aaa.y);
			string strlocation1 = "X:" + to_string(aaa.x) + ", Y:" + to_string(aaa.y);
			Point location2(1125, aaa.y +50);
			string strlocation2 = "Area [" + to_string(i) + "]" + to_string(area);
			putText(img_dst, strlocation1, location1, FONT_HERSHEY_PLAIN, 1, green, 1);
			putText(img_dst, strlocation2, location2, FONT_HERSHEY_PLAIN, 1, green, 1);

			Moments mu;
			mu = moments(contours_right[i]);
			int cx = static_cast<float> (mu.m10 / (mu.m00 + 1e-5));
			int cy = static_cast<float> (mu.m01 / (mu.m00 + 1e-5));
			cx += 1125;
			cy += 180;
			circle(img_dst, Point(cx, cy), 5, blue, -1);
			Point mulocation(cx + 10, cy);
			putText(img_dst, to_string(i), mulocation, FONT_HERSHEY_PLAIN, 1, blue, 1);
		}
	}
	// ===================================================================================================================	
	int left_count = 0;
	vector<int> left_check;
	for (size_t i = 0; i < contours_left.size(); i++)			// left
	{
		drawContours(img_gray_left, contours_left, i, green, 5);
		int area = contourArea(contours_left[i]);

		if (left_count < i)
			left_count = i;
		if (area < 3000)
			left_check.push_back(i);
	}
	if (left_count <= 3)
	{
		for (auto i = 0; i < left_check.size(); i++)
		{
			Rect rect = boundingRect(contours_left[i]);
			Point pt(30, 180);
			rect = rect + pt;
			/*new rect = 1125, 180, 140, 320*/
			rectangle(img_dst, rect, red, 2);
		}
		Point location(img_dst.cols / 2 - 100, img_dst.rows / 2 + 300);
		putText(img_dst, "FAIL : BLOCKED HOLL", location, FONT_HERSHEY_PLAIN, 3, red, 1);
	}
	else
	{
		L_putTR(img_dst);
		for (size_t i = 0; i < contours_left.size(); i++)
		{
			drawContours(img_gray_left, contours_left, i, green, 5);
			int area = contourArea(contours_left[i]);
			Point aaa = contours_left [i] [0] ;
			aaa.x += 30;
			aaa.y += 180;
			Point location1(30, aaa.y);
			string strlocation1 = "X:" + to_string(aaa.x) + ", Y:" + to_string(aaa.y);
			Point location2(30, aaa.y + 50);
			string strlocation2 =  "Area ["+ to_string(i) + "]" + to_string(area);
			putText(img_dst, strlocation1, location1, FONT_HERSHEY_PLAIN, 1, green, 1);
			putText(img_dst, strlocation2, location2, FONT_HERSHEY_PLAIN, 1, green, 1);

			Moments mu;
			mu = moments(contours_left[i]);
			int cx = static_cast<float> (mu.m10 / (mu.m00 + 1e-5));
			int cy = static_cast<float> (mu.m01 / (mu.m00 + 1e-5));
			cx += 30;
			cy += 180;
			circle(img_dst, Point(cx, cy), 5, blue, -1);
			Point mulocation(cx + 10, cy);
			putText(img_dst, to_string(i), mulocation, FONT_HERSHEY_PLAIN, 1, blue, 1);
		}
	}


	//imshow("src", img_src);
	//imshow("gray", img_gray);
	//imshow("bottom", img_gray_bottom);
	imshow("dst", img_dst);

	waitKey(0);
	destroyAllWindows();
	return 0;

}

