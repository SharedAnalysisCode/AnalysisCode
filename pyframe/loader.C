/*
 * loader.C - A file for helping PyROOT deal. Kinda black magic.
 */
#include<vector>
#include<string>
#include<set>

#ifdef __CINT__
#pragma link C++ class vector<string>;
#pragma link C++ class vector<vector<string> >;
#pragma link C++ class vector<vector<int> >;
#pragma link C++ class vector<vector<unsigned int> >;
#pragma link C++ class vector<vector<float> >;
#pragma link C++ class vector<vector<double> >;
#pragma link C++ class pair<set<int>::iterator,bool>;
#else
template class std::vector<std::vector<float> >;
template class std::vector<std::vector<double> >;
#endif
