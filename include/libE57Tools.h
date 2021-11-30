typedef struct {

    int64_t channels;
    int64_t cartesianX;
	int64_t cartesianY;
	int64_t cartesianZ;
	int64_t cartesianInvalidState;
	int64_t intensity;
	int64_t colorRed;
	int64_t colorGreen;
	int64_t colorBlue;
	int64_t columnIndex;
	int64_t rowIndex;
	int64_t BuffersFloatsCount;
	int64_t BuffersIntsCount;

} ToolsFileInfo;

int64_t importfile(char* filename, double *xyz, int64_t *state);
int64_t recordCount(char* filename, ToolsFileInfo* info);