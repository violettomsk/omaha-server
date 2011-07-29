from twisted.python import log
import MySQLdb as mdb
import sys

class MacDbHelper:
  def __init__(self):
    try:
      self.conn = mdb.connect('localhost', 'root', '', 'omaha')
      self.cursor = self.conn.cursor(mdb.cursors.DictCursor)
      self.cursor.execute("CREATE TABLE IF NOT EXISTS \
              MacUpdates(id INT PRIMARY KEY AUTO_INCREMENT, \
                         version VARCHAR(64), \
                         dmg_path VARCHAR(255), \
                         rel_notes TEXT, \
                         dsa_signature VARCHAR(100))")
      self.conn.commit()
    except mdb.Error, e:
      log.msg("MySQL error %d: %s" % (e.args[0],e.args[1]))
      sys.exit(1)
        
  def cleanup(self):
    try:
      self.cursor.close()
      self.conn.close()
    except mdb.Error, e:
      log.msg("MySQL error %d: %s" % (e.args[0],e.args[1]))
      sys.exit(1)
  
  def fetch_latest(self):
    try:
      self.cursor.execute("SELECT * FROM MacUpdates \
                           WHERE version=(SELECT MAX(version) FROM MacUpdates)")
      return self.cursor.fetchone()
    except mdb.Error, e:
      log.msg("MySQL error %d: %s" % (e.args[0],e.args[1]))
      sys.exit(1)
    
    return None
    
  def fetch_several_latest(self, numRecords):
    try:
      self.cursor.execute("SELECT * FROM MacUpdates \
                           ORDER BY version DESC \
                           LIMIT %d" % (numRecords))
      return self.cursor.fetchall()
    except mdb.Error, e:
      log.msg("MySQL error %d: %s" % (e.args[0],e.args[1]))
      sys.exit(1)
    
    return [];
        
  def insert(self, insertInfo):
    try:
      self.cursor.execute("INSERT INTO MacUpdates SET version='%s', dmg_path='%s', rel_notes='%s', dsa_signature='%s'" %
        (mdb.escape_string(insertInfo['version']), 
         mdb.escape_string(insertInfo['dmg_path']),
         mdb.escape_string(insertInfo['rel_notes']),
         mdb.escape_string(insertInfo['dsa_signature'])
        ))
      self.conn.commit()
    except mdb.Error, e:
      log.msg("MySQL error %d: %s" % (e.args[0],e.args[1]))
      sys.exit(1)
    
  def update(self, updateInfo):
    try:
      self.cursor.execute("UPDATE MacUpdates SET version='%s', dmg_path='%s', rel_notes='%s', dsa_signature='%s' \
        WHERE id='%s'" %
        (mdb.escape_string(updateInfo['version']), 
         mdb.escape_string(updateInfo['dmg_path']),
         mdb.escape_string(updateInfo['rel_notes']),
         mdb.escape_string(updateInfo['dsa_signature']),
         mdb.escape_string(updateInfo['id'])
        ))
      self.conn.commit()
    except mdb.Error, e:
      log.msg("MySQL error %d: %s" % (e.args[0],e.args[1]))
      sys.exit(1)
      
  def delete(self, id):
    try:
      self.cursor.execute("DELETE FROM MacUpdates WHERE id='%s'" %
        (mdb.escape_string(id)) 
      )
      self.conn.commit()
    except mdb.Error, e:
      log.msg("MySQL error %d: %s" % (e.args[0],e.args[1]))
      sys.exit(1)        