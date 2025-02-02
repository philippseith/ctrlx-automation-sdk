/**
 * MIT License
 * 
 * Copyright (c) 2021 Bosch Rexroth AG
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

#include <stdio.h>
#include <iostream>

#include "comm/datalayer/datalayer.h"
#include "comm/datalayer/datalayer_system.h"
#include "comm/datalayer/metadata_generated.h"
#include "comm/datalayer/notify_info_generated.h"

class DataLayerClientSub
{
private:
  comm::datalayer::DatalayerSystem _datalayerSystem;

  comm::datalayer::IClient2 *_datalayerClient;

  comm::datalayer::PublishCallback publishCallback();

public:

  DataLayerClientSub(const comm::datalayer::DatalayerSystem &datalayerSystem);

  comm::datalayer::DlResult connect(const std::string &clientConnection);

  comm::datalayer::DlResult isConnected();

  comm::datalayer::DlResult createSubscriptionSync(const std::string &id);

  comm::datalayer::DlResult subscribeSync(const std::string &id, const std::string &address);

  comm::datalayer::DlResult subscribeSync_Multi(const std::string &id, const std::set<std::string> &addresses);

  comm::datalayer::DlResult unsubscribeSync(const std::string &id);

  void disconnect();
};
