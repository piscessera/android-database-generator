package com.piscessera.gen.database;

import java.io.IOException;
import java.io.InputStream;

import android.content.Context;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import com.piscessera.gen.util.ApplicationUtil;
import com.piscessera.gen.util.DebugUtil;
import com.piscessera.gen.util.FileUtil;

public class DatabaseCore extends SQLiteOpenHelper {
private static String DB_PATH = "/data/data/com.piscessera.gen/databases/";

private static String DB_NAME = "gen_db.sqlite";
private static String DB_VERSION = "gen_db_version";

private final Context mContext;
private SQLiteDatabase mDb;

public DatabaseCore(Context context) {
super(context, DB_NAME, null, ApplicationUtil
.getAppVersionCode(context));
this.mContext = context;

FileUtil fileUtil = new FileUtil(context);

int newVersion = ApplicationUtil.getAppVersionCode(context);
int oldVersion = -99;
InputStream in = fileUtil.getContextFile(DB_VERSION);

if (in != null) {
String oldVersionStr = fileUtil.convertIs2String(in);
if (!"".equals(oldVersionStr)) {
oldVersion = Integer.parseInt(oldVersionStr);
}
}

try {
if (oldVersion < newVersion) {
deleteDatabase();
createDatabase();
fileUtil.saveContextFile(DB_VERSION, String.valueOf(newVersion));
DebugUtil.showInfoLog(mContext, "Create database success!");
}
} catch (IOException e) {
e.printStackTrace();
}
}

public SQLiteDatabase getmDb() {
return mDb;
}

private void createDatabase() throws IOException {
boolean dbExist = checkDatabase();
if (dbExist) {

} else {
this.getReadableDatabase();
try {
copyDatabase();
} catch (IOException e) {
throw new Error("Error copying database");
}
}
}

private boolean checkDatabase() {
SQLiteDatabase checkDB = null;
try {
String dbPath = DB_PATH + DB_NAME;
checkDB = SQLiteDatabase.openDatabase(dbPath, null,
SQLiteDatabase.OPEN_READONLY);
} catch (SQLException e) {
e.printStackTrace();
}

if (checkDB != null) {
checkDB.close();
}

return checkDB != null ? true : false;
}

private void copyDatabase() throws IOException {
FileUtil fileUtil = new FileUtil(mContext);
fileUtil.copyAssets(DB_NAME, DB_PATH);
// fileUtil.copyAssets(mContext.getAssets(), DB_PATH);
DebugUtil.showInfoLog(mContext, "Copy database success!");
}

private void deleteDatabase() throws IOException {
FileUtil fileUtil = new FileUtil(mContext);
fileUtil.deleteFileIfExist(DB_PATH + DB_NAME);
DebugUtil.showInfoLog(mContext, "Delete database success!");
}

public void openDatabae() throws SQLException {
String dbPath = DB_PATH + DB_NAME;
mDb = SQLiteDatabase.openDatabase(dbPath, null,
SQLiteDatabase.OPEN_READONLY);
}

@Override
public synchronized void close() {
if (mDb != null) {
mDb.close();
}
super.close();
}

@Override
public void onCreate(SQLiteDatabase db) {
}

@Override
public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
}
}
