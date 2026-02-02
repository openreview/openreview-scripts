/* eslint-disable no-await-in-loop */

import { MongoClient } from 'mongodb';
import dns from 'dns';
import { configLoader } from '../helpers/utils.js';

const { setDefaultResultOrder } = dns;

const config = configLoader({
  ext: 'json',
  env: process.env.NODE_ENV,
});
const { database } = config;

// This allows the client to connect to mongo when using Node 18
setDefaultResultOrder('ipv4first');

function isDomainFromAcademia(domain) {
  if (!domain) {
    return false;
  }

  domain = domain.toLowerCase();

  if (domain.endsWith('.edu')) {
    return true;
  }

  if (domain.includes('.edu.')) {
    return true;
  }

  return false;
}

function belongsToAcademia(profile, currentYear) {
  const history = profile.content?.history || [];
  for (const item of history) {
    const end = item.end;
    const isEndNumber = typeof end === 'number';
    if (!isEndNumber || (isEndNumber && end >= currentYear)) {
      const domain = item.institution?.domain;
      if (isDomainFromAcademia(domain)) {
        return true;
      }
    }
  }
  const emails = profile.content?.emails || [];
  for (const email of emails) {
    const domain = email.split('@').pop();
    if (isDomainFromAcademia(domain)) {
      return true;
    }
  }
  return false;
}

const classifyProfiles = async (databaseName, collectionName, query) => {
  const client = new MongoClient('mongodb://' + database.url, database.options);
  await client.connect();
  const db = client.db(databaseName);
  const cursor = db.collection(collectionName).find(query);

  const numberOfDocuments = await db.collection(collectionName).countDocuments(query);

  const currentYear = new Date().getFullYear();

  let academiaProfiles = 0;

  if (numberOfDocuments === 0) {
    await client.close();
    return numberOfDocuments;
  }

  while (await cursor.hasNext()) {
    const profile = await cursor.next();
    if (belongsToAcademia(profile, currentYear)) {
      academiaProfiles++;
    }
  }

  await client.close();

  console.log(`${academiaProfiles} out of ${numberOfDocuments} profiles belong to academia`);
};

const main = async () => {
  const databaseName = database.name;
  const docsCollection = 'openreview_profiles';
  const query = {
    state: { $regex: /^Active/ },
    ddate: null,
  };
  const filename = 'profiles';

  await classifyProfiles(databaseName, docsCollection, query, filename);
};

main();
