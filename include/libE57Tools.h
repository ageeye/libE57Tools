typedef struct {

    int64_t channels;
    int64_t cartesianX;
	int64_t cartesianY;
	int64_t cartesianZ;
	int64_t cartesianInvalidState;

} ToolsFileInfo;

int64_t importfile(char* filename, double *xyz, int64_t *state);
int64_t recordCount(char* filename, ToolsFileInfo* info);