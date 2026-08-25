rpm.global("commit", gh_commit("TrenchBroom/TrenchBroom"));
if rpm.changed() {
	rpm.release();

	let v = gh("TrenchBroom/TrenchBroom");
	v.crop(1);
	let vre = v.split(".");

	rpm.global("VERSION_YEAR", vre[0]);
	rpm.global("VERSION_NUMBER", vre[1]);

	rpm.global("commit_date", date());
}
