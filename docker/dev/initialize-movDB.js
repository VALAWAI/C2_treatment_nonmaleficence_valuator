db.createUser({
	user: process.env.MOV_DB_USER_NAME,
	pwd: process.env.MOV_DB_USER_PASSWORD,
	roles: [{
		role: 'readWrite',
		db: process.env.MOV_DB_NAME
	}]
})
