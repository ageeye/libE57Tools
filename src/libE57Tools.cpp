// this based on:
// $Id: e57unpack.cpp 338 2013-09-03 12:36:09Z roland_schwarz $

#include <E57Format.h>
using e57::Node;
using e57::ImageFile;
using e57::StructureNode;
using e57::VectorNode;
using e57::CompressedVectorNode;
using e57::StringNode;
using e57::IntegerNode;
using e57::ScaledIntegerNode;
using e57::FloatNode;
using e57::StringNode;
using e57::BlobNode;
using e57::E57Exception;
using e57::ustring;
using e57::SourceDestBuffer;
using e57::CompressedVectorReader;
using e57::int64_t;
using e57::uint64_t;
using e57::uint8_t;

#include <iostream>
using std::cout;
using std::cerr;
using std::endl;
using std::ostream;
using std::ios_base;
using std::streamsize;

#include <exception>
using std::exception;

#include <stdexcept>
using std::runtime_error;

#if defined(_MSC_VER) || defined(__APPLE__)
#   include <memory>
#else
#   include <tr1/memory>
#endif
#ifdef __APPLE__
using std::shared_ptr;
#else
using std::tr1::shared_ptr;
#endif

#include <string>
using std::string;

#include <vector>
using std::vector;

#include <limits>
using std::numeric_limits;

#ifdef __cplusplus
extern "C" {
#endif
#include "libE57Tools.h" 

// In first step we count the records. This implementation is bad, because the
// xml part contains this information. 

int64_t recordCount(char* filename, ToolsFileInfo* info)
{
	ImageFile imf(std::string(filename), "r");
	StructureNode root = imf.root();
	uint64_t total_count(0);
	if (root.isDefined("data3D")) {
		VectorNode data3D(root.get("data3D"));
		for (int64_t child=0; child<data3D.childCount(); ++child) {
            StructureNode            scan(data3D.get(child));
            CompressedVectorNode     points(scan.get("points"));
            StructureNode            prototype(points.prototype());
            vector<SourceDestBuffer> sdb;
            const size_t buf_size = 1024;
			static const size_t buflen = prototype.childCount();
			double* fbuf = new double[buflen * buf_size];
			int64_t* ibuf = new int64_t[buflen * buf_size];
			
			info->channels = prototype.childCount();
			info->BuffersFloatsCount = 0;
			info->BuffersIntsCount = 0;
			
            for (int i=0; i<prototype.childCount(); ++i) {
                Node n(prototype.get(i));
				
				if (n.elementName()=="cartesianX") {
					info->cartesianX = i;
				}
				
				if (n.elementName()=="cartesianY") {
					info->cartesianY = i;
				}
		
				if (n.elementName()=="cartesianZ") {
					info->cartesianZ = i;
				}
				
				if (n.elementName()=="cartesianInvalidState") {
					info->cartesianInvalidState = i;
				}
				if (n.elementName()=="intensity") {
					info->intensity = i;
				}
				if (n.elementName()=="colorRed") {
					info->colorRed= i;
				}
				if (n.elementName()=="colorGreen") {
					info->colorGreen = i;
				}
				if (n.elementName()=="colorBlue") {
					info->colorBlue = i;
				}
				if (n.elementName()=="columnIndex") {
					info->columnIndex = i;
				}
				if (n.elementName()=="rowIndex") {
					info->rowIndex = i;
				}

                switch(n.type()) {
                    case e57::E57_FLOAT:
                    case e57::E57_SCALED_INTEGER:
						info->BuffersFloatsCount++;
                        sdb.push_back(
                            SourceDestBuffer(
                                imf
                                , n.elementName()
                                , &(fbuf[i*buf_size])
                                , buf_size
                                , true
                                , true
                            )
                        );
                        break;
                    case e57::E57_INTEGER:
						info->BuffersIntsCount++;
                        sdb.push_back(
                            SourceDestBuffer(
                                imf
                                , n.elementName()
                                , &(ibuf[i*buf_size])
                                , buf_size
                                , true
                                , true
                            )
                        );
                    break;
                    default:
                        return -1;
                }
            }
			
            unsigned count;
			
			CompressedVectorReader rd(points.reader(sdb));
			
            while(count = rd.read()) {
                total_count += count;
            }
		} 
	}
	return total_count;
	
}

int64_t importfile(char* filename, double *xyz, int64_t *state)
{
	ImageFile imf(std::string(filename), "r");
	StructureNode root = imf.root();
	uint64_t total_count(0);
	if (root.isDefined("data3D")) {
		VectorNode data3D(root.get("data3D"));
		for (int64_t child=0; child<data3D.childCount(); ++child) {
            StructureNode            scan(data3D.get(child));
            CompressedVectorNode     points(scan.get("points"));
            StructureNode            prototype(points.prototype());
            vector<SourceDestBuffer> sdb;
            const size_t buf_size = 1024;
			static const size_t buflen = prototype.childCount();
			double* fbuf = new double[buflen * buf_size];
			int64_t* ibuf = new int64_t[buflen * buf_size];
			bool* tbuf = new bool[buflen];
			
            for (int i=0; i<prototype.childCount(); ++i) {
                Node n(prototype.get(i));

                switch(n.type()) {
                    case e57::E57_FLOAT:
                    case e57::E57_SCALED_INTEGER:
						tbuf[i] = true;
                        sdb.push_back(
                            SourceDestBuffer(
                                imf
                                , n.elementName()
                                , &(fbuf[i*buf_size])
                                , buf_size
                                , true
                                , true
                            )
                        );
                        break;
                    case e57::E57_INTEGER:
						tbuf[i] = false;
                        sdb.push_back(
                            SourceDestBuffer(
                                imf
                                , n.elementName()
                                , &(ibuf[i*buf_size])
                                , buf_size
                                , true
                                , true
                            )
                        );
                    break;
                    default:
                        return -1;
                }
            }
			
            unsigned count;
			unsigned fpos=0;
			unsigned ipos=0;
			
			CompressedVectorReader rd(points.reader(sdb));
			
            while(count = rd.read()) {
                total_count += count;
                for (size_t i=0; i<count; ++i) {
                     for (size_t j=0; j<buflen; ++j)
                         if (tbuf[j]) {
                         	xyz[fpos++] = fbuf[j*buf_size+i];
                         }
					 	else {
							state[ipos++] = ibuf[j*buf_size+i];
					 	}
                 }
            }
		} 
	}
	return total_count;
    
}

#ifdef __cplusplus
}
#endif
