#include <iostream>
std::pair<unsigned long long, unsigned long long> reduction(std::pair<unsigned long long, unsigned long long> x) {
	unsigned long long n = x.first;
	while (n > 1) { //���ڰ� 1���� Ŭ �� ���� ����
		if (x.first % n == 0 && x.second % n == 0) {
			x.first /= n;
			x.second /= n;
			n = x.first;
		}
		else
			n--;
	}
	return x;
}
std::pair<unsigned long long, unsigned long long> substract(std::pair<unsigned long long, unsigned long long> x, std::pair<unsigned long long, unsigned long long> y) {
	unsigned long long temp = y.second;
	y.first *= x.second;
	y.second *= x.second;
	x.first *= temp;
	x.second *= temp; //���
	x.first -= y.first; //���ڳ��� ����
	return reduction(x);
}
std::pair<unsigned long long, unsigned long long> egyptian(std::pair<unsigned long long, unsigned long long> x) {
	unsigned long long denominator;
	denominator = x.second / x.first;
	if (x.second % x.first != 0)
		denominator++;
	//std::cout << "(1 / " << denominator << ")" << std::endl;
	return substract(x, std::pair<unsigned long long, unsigned long long>(1, denominator));
}
int main() {
	std::pair<unsigned long long, unsigned long long> fraction; //first: p second: q
	int result = 0;
	std::cin >> fraction.first >> fraction.second;
	while (fraction.first > 0) {
		fraction = egyptian(fraction);
		result++;
	}
	std::cout << result << std::endl;
}